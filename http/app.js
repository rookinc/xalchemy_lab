const state = {
  settings: [],
  workspaces: [],
  navItems: [],
  toolGroups: [],
  toolItems: [],
  contentEntries: [],
  activeWorkspaceKey: null,
  activeEntryKey: null,
};

const el = {
  brandBlock: document.getElementById("brand-block"),
  globalNav: document.getElementById("global-nav"),
  toolRail: document.getElementById("tool-rail"),
  moduleHost: document.getElementById("module-host"),
  statusText: document.getElementById("status-text"),
};

async function apiGet(path) {
  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API ${response.status}: ${text}`);
  }

  return response.json();
}

async function loadBootstrap() {
  const data = await apiGet("/api/bootstrap");

  state.settings = data.app_settings ?? [];
  state.workspaces = data.workspace_modules ?? [];
  state.navItems = data.global_nav_items ?? [];
  state.toolGroups = data.tool_groups ?? [];
  state.toolItems = data.tool_items ?? [];
  state.contentEntries = data.content_entries ?? [];

  state.activeWorkspaceKey =
    getSetting("default_workspace") ||
    getNavItems()[0]?.nav_key ||
    null;

  const workspace = getWorkspaceByKey(state.activeWorkspaceKey);
  state.activeEntryKey = workspace
    ? getDefaultContentEntryForWorkspace(workspace.id)?.entry_key ?? null
    : null;
}

function getSetting(settingKey, fallback = null) {
  const row = state.settings.find((x) => x.setting_key === settingKey);
  return row ? row.setting_value : fallback;
}

function getWorkspaceByKey(moduleKey) {
  return (
    state.workspaces.find(
      (x) => x.module_key === moduleKey && Number(x.is_active) === 1
    ) || null
  );
}

function getNavItems() {
  return [...state.navItems]
    .filter((x) => Number(x.is_active) === 1)
    .sort((a, b) => a.sort_order - b.sort_order);
}

function getToolGroupsForWorkspace(workspaceId) {
  return [...state.toolGroups]
    .filter(
      (x) =>
        Number(x.workspace_module_id) === Number(workspaceId) &&
        Number(x.is_active) === 1
    )
    .sort((a, b) => a.sort_order - b.sort_order);
}

function getToolItemsForGroup(groupId) {
  return [...state.toolItems]
    .filter(
      (x) =>
        Number(x.tool_group_id) === Number(groupId) &&
        Number(x.is_active) === 1
    )
    .sort((a, b) => a.sort_order - b.sort_order);
}

function getDefaultContentEntryForWorkspace(workspaceId) {
  return (
    [...state.contentEntries]
      .filter(
        (x) =>
          Number(x.workspace_module_id) === Number(workspaceId) &&
          x.status === "published"
      )
      .sort((a, b) => {
        if (Number(b.is_default) !== Number(a.is_default)) {
          return Number(b.is_default) - Number(a.is_default);
        }
        return a.sort_order - b.sort_order;
      })[0] || null
  );
}

function getContentEntry(workspaceId, entryKey) {
  return (
    state.contentEntries.find(
      (x) =>
        Number(x.workspace_module_id) === Number(workspaceId) &&
        x.entry_key === entryKey &&
        x.status === "published"
    ) || null
  );
}

function parseActionPayload(payload) {
  if (!payload) return null;
  if (typeof payload === "object") return payload;

  try {
    return JSON.parse(payload);
  } catch {
    return null;
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttr(value) {
  return escapeHtml(value);
}

function renderBrand() {
  const title = getSetting("site_title", "Aletheos");
  const tagline = getSetting("site_tagline", "Dynamic workspace shell");

  el.brandBlock.innerHTML = `
    <h1>${escapeHtml(title)}</h1>
    <p>${escapeHtml(tagline)}</p>
  `;
}

function renderGlobalNav() {
  const items = getNavItems();

  el.globalNav.innerHTML = `
    <label for="global-nav-select">Global Nav</label>
    <select id="global-nav-select">
      ${items
        .map(
          (item) => `
            <option value="${escapeAttr(item.nav_key)}" ${
              item.nav_key === state.activeWorkspaceKey ? "selected" : ""
            }>
              ${escapeHtml(item.label)}
            </option>
          `
        )
        .join("")}
    </select>
  `;

  const select = document.getElementById("global-nav-select");
  select.addEventListener("change", () => {
    state.activeWorkspaceKey = select.value;

    const workspace = getWorkspaceByKey(state.activeWorkspaceKey);
    state.activeEntryKey = workspace
      ? getDefaultContentEntryForWorkspace(workspace.id)?.entry_key ?? null
      : null;

    renderApp();
  });
}

function renderToolRail() {
  const workspace = getWorkspaceByKey(state.activeWorkspaceKey);

  if (!workspace) {
    el.toolRail.innerHTML = "";
    return;
  }

  const groups = getToolGroupsForWorkspace(workspace.id);

  el.toolRail.innerHTML = groups
    .map((group) => {
      const items = getToolItemsForGroup(group.id);

      return `
        <div class="toolset-block">
          <h2>${escapeHtml(group.label)}</h2>
          ${items
            .map((item) => {
              const payload = parseActionPayload(item.action_payload);
              const targetKey = payload?.target_entry_key ?? null;
              const active =
                targetKey && targetKey === state.activeEntryKey ? " active" : "";

              return `
                <button
                  class="tool-btn${active}"
                  type="button"
                  data-item-key="${escapeAttr(item.item_key)}"
                >
                  ${escapeHtml(item.label)}
                </button>
              `;
            })
            .join("")}
        </div>
      `;
    })
    .join("");

  el.toolRail.querySelectorAll(".tool-btn").forEach((button) => {
    button.addEventListener("click", () => {
      handleToolClick(button.dataset.itemKey);
    });
  });
}

function handleToolClick(itemKey) {
  const workspace = getWorkspaceByKey(state.activeWorkspaceKey);
  if (!workspace) return;

  const groupIds = getToolGroupsForWorkspace(workspace.id).map((g) => Number(g.id));

  const item =
    state.toolItems.find(
      (x) =>
        groupIds.includes(Number(x.tool_group_id)) &&
        x.item_key === itemKey &&
        Number(x.is_active) === 1
    ) || null;

  if (!item) return;

  const payload = parseActionPayload(item.action_payload);

  if (payload?.action === "load_content" && payload?.target_entry_key) {
    state.activeEntryKey = payload.target_entry_key;
    renderApp();
    return;
  }

  el.statusText.textContent = `Status: ${item.label} clicked.`;
}

function renderContentModule(workspace) {
  const entry = state.activeEntryKey
    ? getContentEntry(workspace.id, state.activeEntryKey)
    : getDefaultContentEntryForWorkspace(workspace.id);

  if (!entry) {
    el.moduleHost.innerHTML = `
      <section class="content-module">
        <h2>${escapeHtml(workspace.label)}</h2>
        <p>No published content found for this workspace.</p>
      </section>
    `;
    return;
  }

  el.moduleHost.innerHTML = `
    <section class="content-module">
      <h2>${escapeHtml(entry.title)}</h2>
      <div>${entry.body_html || ""}</div>
    </section>
  `;
}

function renderCubeModule() {
  el.moduleHost.innerHTML = `
    <section class="content-module">
      <h2>Cube View</h2>
      <div class="cube-stage">
        <div class="cube">
          <div class="face front">1</div>
          <div class="face back">2</div>
          <div class="face right">3</div>
          <div class="face left">4</div>
          <div class="face top">5</div>
          <div class="face bottom">6</div>
        </div>
      </div>
      <p>Placeholder CSS cube. Later this becomes a real 3D renderer.</p>
    </section>
  `;
}

function renderDashboardModule() {
  el.moduleHost.innerHTML = `
    <section class="module-header">
      <div>
        <h2>System • Catalog</h2>
        <p>Dashboard module prototype</p>
      </div>
      <div class="module-actions">
        <button type="button">Refresh</button>
        <button type="button">New</button>
      </div>
    </section>

    <section class="dashboard-grid">
      <div class="panel dashboard-nav-panel">
        <h3>Sections</h3>
        <div class="stack-list">
          <button class="nav-chip active" type="button">Manufacturers</button>
          <button class="nav-chip" type="button">Canopies</button>
          <button class="nav-chip" type="button">Linesets</button>
          <button class="nav-chip" type="button">Materials</button>
        </div>
      </div>

      <div class="panel dashboard-list-panel">
        <div class="panel-toolbar">
          <strong>Manufacturers</strong>
          <div class="toolbar-row">
            <input type="text" placeholder="Search" />
            <button type="button">Clear</button>
          </div>
        </div>

        <div class="table-shell">
          <div class="table-header">
            <span>Name</span>
            <span>Status</span>
          </div>
          <div class="table-body">
            <button class="table-row active" type="button">
              <span>NZ Aerosports</span>
              <span>Active</span>
            </button>
            <button class="table-row" type="button">
              <span>TrimSetter</span>
              <span>Active</span>
            </button>
            <button class="table-row" type="button">
              <span>Test Vendor</span>
              <span>Inactive</span>
            </button>
          </div>
        </div>
      </div>

      <div class="panel dashboard-detail-panel">
        <div class="panel-toolbar">
          <strong>Details</strong>
        </div>

        <form class="detail-form">
          <label>
            <span>Manufacturer</span>
            <input type="text" value="NZ Aerosports" />
          </label>

          <label>
            <span>Short Code</span>
            <input type="text" value="NZA" />
          </label>

          <label class="checkbox-row">
            <input type="checkbox" checked />
            <span>Active</span>
          </label>

          <label>
            <span>Notes</span>
            <textarea rows="6">Example detail pane for a future dashboard module.</textarea>
          </label>

          <div class="form-actions">
            <button type="button">Save</button>
            <button type="button">Create</button>
          </div>
        </form>
      </div>

      <div class="panel dashboard-bottom-panel">
        <div class="panel-toolbar">
          <strong>Lower Pane</strong>
        </div>
        <p>This area can host logs, child editors, history, previews, or line-set tools.</p>
      </div>
    </section>
  `;
}

function renderModuleHost() {
  const workspace = getWorkspaceByKey(state.activeWorkspaceKey);

  if (!workspace) {
    el.moduleHost.innerHTML = "<p>No active workspace.</p>";
    return;
  }

  if (workspace.module_key === "cube") {
    renderCubeModule();
    return;
  }

  if (workspace.module_key === "dashboard") {
    renderDashboardModule();
    return;
  }

  renderContentModule(workspace);
}

function renderStatus() {
  const workspace = getWorkspaceByKey(state.activeWorkspaceKey);
  el.statusText.textContent = workspace
    ? `Status: ${workspace.label} loaded.`
    : "Status: ready.";
}

function renderApp() {
  renderBrand();
  renderGlobalNav();
  renderToolRail();
  renderModuleHost();
  renderStatus();
}

async function initApp() {
  try {
    await loadBootstrap();
    renderApp();
  } catch (error) {
    console.error(error);
    el.statusText.textContent = `Status: ${error.message}`;
    el.moduleHost.innerHTML = `
      <section class="content-module">
        <h2>Startup Error</h2>
        <p>${escapeHtml(error.message)}</p>
      </section>
    `;
  }
}

initApp();
