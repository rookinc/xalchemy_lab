-- MySQL dump 10.13  Distrib 9.3.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: aletheos
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_settings`
--

DROP TABLE IF EXISTS `app_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_settings` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` text COLLATE utf8mb4_unicode_ci,
  `setting_type` enum('text','json','number','boolean') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'text',
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_app_settings_key` (`setting_key`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_settings`
--

LOCK TABLES `app_settings` WRITE;
/*!40000 ALTER TABLE `app_settings` DISABLE KEYS */;
INSERT INTO `app_settings` VALUES (1,'site_title','Alchemy Lab','text','Displayed in the shell header','2026-03-25 12:43:46','2026-03-25 12:43:46'),(2,'default_workspace','html','text','Initial workspace module key','2026-03-25 12:43:46','2026-03-25 12:43:46'),(3,'theme_mode','dark','text','Initial UI theme','2026-03-25 12:43:46','2026-03-25 12:43:46'),(4,'site_tagline','Dynamic workspace shell','text','Displayed under the site title','2026-03-25 13:41:17','2026-03-25 13:41:17');
/*!40000 ALTER TABLE `app_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_entries`
--

DROP TABLE IF EXISTS `content_entries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `content_entries` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `workspace_module_id` bigint unsigned NOT NULL,
  `parent_entry_id` bigint unsigned DEFAULT NULL,
  `entry_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `entry_type` enum('page','topic','article','panel','doc') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'page',
  `slug` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `body_html` longtext COLLATE utf8mb4_unicode_ci,
  `body_json` json DEFAULT NULL,
  `status` enum('draft','published','archived') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'draft',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `sort_order` int NOT NULL DEFAULT '100',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_content_entries_module_key` (`workspace_module_id`,`entry_key`),
  UNIQUE KEY `uq_content_entries_slug` (`slug`),
  KEY `idx_content_entries_module_status_sort` (`workspace_module_id`,`status`,`sort_order`),
  KEY `idx_content_entries_parent` (`parent_entry_id`),
  CONSTRAINT `fk_content_entries_parent` FOREIGN KEY (`parent_entry_id`) REFERENCES `content_entries` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_content_entries_workspace` FOREIGN KEY (`workspace_module_id`) REFERENCES `workspace_modules` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_entries`
--

LOCK TABLES `content_entries` WRITE;
/*!40000 ALTER TABLE `content_entries` DISABLE KEYS */;
INSERT INTO `content_entries` VALUES (1,1,NULL,'home','Hello World Site','page','home','<p>This body panel can host normal HTML content.</p><p>Right now this is a clean framework shell inside <code>alchemy_lab/http</code>.</p>',NULL,'published',1,10,'2026-03-25 12:57:07','2026-03-25 12:57:07'),(2,9,NULL,'dashboard','Dashboard Help','topic','help-dashboard','<p>The dashboard workspace is for browsing structured records, editing details, and working in multi-pane admin views.</p><p>Use the left rail to move between task groups and the main body to inspect or edit data.</p>',NULL,'published',1,10,'2026-03-25 12:57:07','2026-03-25 12:57:07'),(3,9,NULL,'3d-viewer','3D Viewer Help','topic','help-3d-viewer','<p>The 3D viewer workspace is for interactive visual inspection.</p><p>Later this can host a real WebGL or Three.js scene with drag rotation, camera controls, and object selection.</p>',NULL,'published',0,20,'2026-03-25 12:57:07','2026-03-25 12:57:07'),(4,9,NULL,'general','General Help','topic','help-general','<p>This application shell is designed to host multiple workspace types inside one consistent frame.</p><p>Global navigation selects the active workspace. The left rail provides contextual tools. The body panel hosts the active module content.</p>',NULL,'published',0,30,'2026-03-25 12:58:27','2026-03-25 12:58:27');
/*!40000 ALTER TABLE `content_entries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `global_nav_items`
--

DROP TABLE IF EXISTS `global_nav_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `global_nav_items` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `workspace_module_id` bigint unsigned NOT NULL,
  `label` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nav_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '100',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_global_nav_items_key` (`nav_key`),
  KEY `idx_global_nav_items_active_sort` (`is_active`,`sort_order`),
  KEY `fk_global_nav_workspace_module` (`workspace_module_id`),
  CONSTRAINT `fk_global_nav_workspace_module` FOREIGN KEY (`workspace_module_id`) REFERENCES `workspace_modules` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `global_nav_items`
--

LOCK TABLES `global_nav_items` WRITE;
/*!40000 ALTER TABLE `global_nav_items` DISABLE KEYS */;
INSERT INTO `global_nav_items` VALUES (1,1,'HTML View','html',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(2,2,'Cube View','cube',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(3,3,'Dashboard View','dashboard',NULL,1,30,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(4,4,'About','about',NULL,1,40,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(9,9,'Help','help',NULL,1,50,'2026-03-25 12:56:07','2026-03-25 12:56:07');
/*!40000 ALTER TABLE `global_nav_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_actions`
--

DROP TABLE IF EXISTS `graph_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_actions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_kind` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `handler_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `params_json` json DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `action_key` (`action_key`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_actions`
--

LOCK TABLES `graph_actions` WRITE;
/*!40000 ALTER TABLE `graph_actions` DISABLE KEYS */;
INSERT INTO `graph_actions` VALUES (1,'drag_node','Drag Node','layout','drag_node','Drag a node in the spring view.',NULL,'active'),(2,'freeze_layout','Freeze Layout','layout','freeze_layout','Stop the solver and inspect the settled layout.',NULL,'active'),(3,'toggle_labels','Toggle Labels','inspect','toggle_labels','Show or hide node labels.',NULL,'active'),(4,'highlight_outer_cycle','Highlight Outer Cycle','inspect','highlight_outer_cycle','Highlight the outer 5-cycle.',NULL,'active'),(5,'highlight_spokes','Highlight Spokes','inspect','highlight_spokes','Highlight spoke edges.',NULL,'active'),(6,'highlight_inner_star','Highlight Inner Star','inspect','highlight_inner_star','Highlight inner star edges.',NULL,'active');
/*!40000 ALTER TABLE `graph_actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_edges`
--

DROP TABLE IF EXISTS `graph_edges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_edges` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_id` bigint NOT NULL,
  `source_node_id` bigint NOT NULL,
  `target_node_id` bigint NOT NULL,
  `edge_key` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `edge_class` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payload_json` json DEFAULT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_graph_edges_graph` (`graph_id`),
  KEY `fk_graph_edges_source` (`source_node_id`),
  KEY `fk_graph_edges_target` (`target_node_id`),
  CONSTRAINT `fk_graph_edges_graph` FOREIGN KEY (`graph_id`) REFERENCES `graphs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_graph_edges_source` FOREIGN KEY (`source_node_id`) REFERENCES `graph_nodes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_graph_edges_target` FOREIGN KEY (`target_node_id`) REFERENCES `graph_nodes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_edges`
--

LOCK TABLES `graph_edges` WRITE;
/*!40000 ALTER TABLE `graph_edges` DISABLE KEYS */;
INSERT INTO `graph_edges` VALUES (16,1,1,2,'e_outer_0','outer_cycle',NULL,0),(17,1,2,3,'e_outer_1','outer_cycle',NULL,1),(18,1,3,4,'e_outer_2','outer_cycle',NULL,2),(19,1,4,5,'e_outer_3','outer_cycle',NULL,3),(20,1,5,1,'e_outer_4','outer_cycle',NULL,4),(21,1,1,6,'e_spoke_0','spoke',NULL,10),(22,1,2,7,'e_spoke_1','spoke',NULL,11),(23,1,3,8,'e_spoke_2','spoke',NULL,12),(24,1,4,9,'e_spoke_3','spoke',NULL,13),(25,1,5,10,'e_spoke_4','spoke',NULL,14),(26,1,6,8,'e_inner_0','inner_star',NULL,20),(27,1,8,10,'e_inner_1','inner_star',NULL,21),(28,1,10,7,'e_inner_2','inner_star',NULL,22),(29,1,7,9,'e_inner_3','inner_star',NULL,23),(30,1,9,6,'e_inner_4','inner_star',NULL,24);
/*!40000 ALTER TABLE `graph_edges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_nodes`
--

DROP TABLE IF EXISTS `graph_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_nodes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_id` bigint NOT NULL,
  `node_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payload_json` json DEFAULT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_graph_node` (`graph_id`,`node_key`),
  CONSTRAINT `fk_graph_nodes_graph` FOREIGN KEY (`graph_id`) REFERENCES `graphs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_nodes`
--

LOCK TABLES `graph_nodes` WRITE;
/*!40000 ALTER TABLE `graph_nodes` DISABLE KEYS */;
INSERT INTO `graph_nodes` VALUES (1,1,'v0','0',NULL,0),(2,1,'v1','1',NULL,1),(3,1,'v2','2',NULL,2),(4,1,'v3','3',NULL,3),(5,1,'v4','4',NULL,4),(6,1,'v5','5',NULL,5),(7,1,'v6','6',NULL,6),(8,1,'v7','7',NULL,7),(9,1,'v8','8',NULL,8),(10,1,'v9','9',NULL,9);
/*!40000 ALTER TABLE `graph_nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_view_actions`
--

DROP TABLE IF EXISTS `graph_view_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_view_actions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_view_id` bigint NOT NULL,
  `graph_action_id` bigint NOT NULL,
  `is_enabled` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '0',
  `constraints_json` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_graph_view_action` (`graph_view_id`,`graph_action_id`),
  KEY `fk_graph_view_actions_action` (`graph_action_id`),
  CONSTRAINT `fk_graph_view_actions_action` FOREIGN KEY (`graph_action_id`) REFERENCES `graph_actions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_graph_view_actions_view` FOREIGN KEY (`graph_view_id`) REFERENCES `graph_views` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_view_actions`
--

LOCK TABLES `graph_view_actions` WRITE;
/*!40000 ALTER TABLE `graph_view_actions` DISABLE KEYS */;
INSERT INTO `graph_view_actions` VALUES (1,1,1,1,0,NULL),(2,1,2,1,1,NULL),(3,1,6,1,5,NULL),(4,1,4,1,3,NULL),(5,1,5,1,4,NULL),(6,1,3,1,2,NULL);
/*!40000 ALTER TABLE `graph_view_actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_view_edges`
--

DROP TABLE IF EXISTS `graph_view_edges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_view_edges` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_view_id` bigint NOT NULL,
  `graph_edge_id` bigint NOT NULL,
  `style_json` json DEFAULT NULL,
  `is_visible` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_graph_view_edge` (`graph_view_id`,`graph_edge_id`),
  KEY `fk_graph_view_edges_edge` (`graph_edge_id`),
  CONSTRAINT `fk_graph_view_edges_edge` FOREIGN KEY (`graph_edge_id`) REFERENCES `graph_edges` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_graph_view_edges_view` FOREIGN KEY (`graph_view_id`) REFERENCES `graph_views` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_view_edges`
--

LOCK TABLES `graph_view_edges` WRITE;
/*!40000 ALTER TABLE `graph_view_edges` DISABLE KEYS */;
INSERT INTO `graph_view_edges` VALUES (1,1,16,'{\"stroke\": \"#7cc4ff\", \"lineWidth\": 2.5}',1),(2,1,17,'{\"stroke\": \"#7cc4ff\", \"lineWidth\": 2.5}',1),(3,1,18,'{\"stroke\": \"#7cc4ff\", \"lineWidth\": 2.5}',1),(4,1,19,'{\"stroke\": \"#7cc4ff\", \"lineWidth\": 2.5}',1),(5,1,20,'{\"stroke\": \"#7cc4ff\", \"lineWidth\": 2.5}',1),(6,1,21,'{\"stroke\": \"#ffd166\", \"lineWidth\": 2.0}',1),(7,1,22,'{\"stroke\": \"#ffd166\", \"lineWidth\": 2.0}',1),(8,1,23,'{\"stroke\": \"#ffd166\", \"lineWidth\": 2.0}',1),(9,1,24,'{\"stroke\": \"#ffd166\", \"lineWidth\": 2.0}',1),(10,1,25,'{\"stroke\": \"#ffd166\", \"lineWidth\": 2.0}',1),(11,1,26,'{\"stroke\": \"#ff7aa2\", \"lineWidth\": 2.5}',1),(12,1,27,'{\"stroke\": \"#ff7aa2\", \"lineWidth\": 2.5}',1),(13,1,28,'{\"stroke\": \"#ff7aa2\", \"lineWidth\": 2.5}',1),(14,1,29,'{\"stroke\": \"#ff7aa2\", \"lineWidth\": 2.5}',1),(15,1,30,'{\"stroke\": \"#ff7aa2\", \"lineWidth\": 2.5}',1);
/*!40000 ALTER TABLE `graph_view_edges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_view_nodes`
--

DROP TABLE IF EXISTS `graph_view_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_view_nodes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_view_id` bigint NOT NULL,
  `graph_node_id` bigint NOT NULL,
  `x` double DEFAULT NULL,
  `y` double DEFAULT NULL,
  `z` double DEFAULT NULL,
  `pinned` tinyint(1) NOT NULL DEFAULT '0',
  `style_json` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_graph_view_node` (`graph_view_id`,`graph_node_id`),
  KEY `fk_graph_view_nodes_node` (`graph_node_id`),
  CONSTRAINT `fk_graph_view_nodes_node` FOREIGN KEY (`graph_node_id`) REFERENCES `graph_nodes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_graph_view_nodes_view` FOREIGN KEY (`graph_view_id`) REFERENCES `graph_views` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_view_nodes`
--

LOCK TABLES `graph_view_nodes` WRITE;
/*!40000 ALTER TABLE `graph_view_nodes` DISABLE KEYS */;
INSERT INTO `graph_view_nodes` VALUES (1,1,1,180,0,0,0,NULL),(2,1,2,55,171,0,0,NULL),(3,1,3,-145,106,0,0,NULL),(4,1,4,-145,-106,0,0,NULL),(5,1,5,55,-171,0,0,NULL),(6,1,6,90,0,0,0,NULL),(7,1,7,28,86,0,0,NULL),(8,1,8,-72,53,0,0,NULL),(9,1,9,-72,-53,0,0,NULL),(10,1,10,28,-86,0,0,NULL);
/*!40000 ALTER TABLE `graph_view_nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_views`
--

DROP TABLE IF EXISTS `graph_views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_views` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_id` bigint NOT NULL,
  `view_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `view_kind` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `renderer_key` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `params_json` json DEFAULT NULL,
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_graph_view` (`graph_id`,`view_key`),
  CONSTRAINT `fk_graph_views_graph` FOREIGN KEY (`graph_id`) REFERENCES `graphs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_views`
--

LOCK TABLES `graph_views` WRITE;
/*!40000 ALTER TABLE `graph_views` DISABLE KEYS */;
INSERT INTO `graph_views` VALUES (1,1,'spring_debug','Spring Debug','spring_2d','canvas_2d','{\"damping\": 0.85, \"springK\": 0.01, \"maxSpeed\": 12, \"centering\": 0.002, \"repulsion\": 9000, \"nodeRadius\": 10, \"springLength\": 120}',1,'active');
/*!40000 ALTER TABLE `graph_views` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graphs`
--

DROP TABLE IF EXISTS `graphs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graphs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `graph_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `graph_kind` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `graph_key` (`graph_key`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graphs`
--

LOCK TABLES `graphs` WRITE;
/*!40000 ALTER TABLE `graphs` DISABLE KEYS */;
INSERT INTO `graphs` VALUES (1,'petersen','Petersen Graph','Debug graph for spring-layout rendering and view/action plumbing.','petersen','active','2026-03-25 17:58:55','2026-03-25 17:58:55');
/*!40000 ALTER TABLE `graphs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tool_groups`
--

DROP TABLE IF EXISTS `tool_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tool_groups` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `workspace_module_id` bigint unsigned NOT NULL,
  `group_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '100',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tool_groups_key` (`workspace_module_id`,`group_key`),
  KEY `idx_tool_groups_active_sort` (`workspace_module_id`,`is_active`,`sort_order`),
  CONSTRAINT `fk_tool_groups_workspace_module` FOREIGN KEY (`workspace_module_id`) REFERENCES `workspace_modules` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tool_groups`
--

LOCK TABLES `tool_groups` WRITE;
/*!40000 ALTER TABLE `tool_groups` DISABLE KEYS */;
INSERT INTO `tool_groups` VALUES (1,4,'primary-tools','Tools',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(2,2,'primary-tools','Tools',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(3,3,'primary-tools','Tools',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(4,1,'primary-tools','Tools',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(8,2,'selection-tools','Selection',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(9,3,'selection-tools','Selection',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(10,1,'selection-tools','Selection',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(13,9,'help-topics','Help Topics',NULL,1,10,'2026-03-25 12:56:14','2026-03-25 12:56:14');
/*!40000 ALTER TABLE `tool_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tool_items`
--

DROP TABLE IF EXISTS `tool_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tool_items` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `tool_group_id` bigint unsigned NOT NULL,
  `item_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_type` enum('ui','route','api','modal','external','noop') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ui',
  `action_payload` json DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '100',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tool_items_key` (`tool_group_id`,`item_key`),
  KEY `idx_tool_items_active_sort` (`tool_group_id`,`is_active`,`sort_order`),
  CONSTRAINT `fk_tool_items_group` FOREIGN KEY (`tool_group_id`) REFERENCES `tool_groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tool_items`
--

LOCK TABLES `tool_items` WRITE;
/*!40000 ALTER TABLE `tool_items` DISABLE KEYS */;
INSERT INTO `tool_items` VALUES (1,4,'inspect','Inspect','ui',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(2,2,'inspect','Inspect','ui',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(3,3,'inspect','Inspect','ui',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(4,1,'inspect','Inspect','ui',NULL,1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(8,4,'refresh','Refresh','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(9,2,'refresh','Refresh','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(10,3,'refresh','Refresh','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(11,1,'refresh','Refresh','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(15,10,'history','History','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(16,8,'history','History','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(17,9,'history','History','ui',NULL,1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(18,10,'notes','Notes','ui',NULL,1,30,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(19,8,'notes','Notes','ui',NULL,1,30,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(20,9,'notes','Notes','ui',NULL,1,30,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(23,4,'settings','Settings','ui',NULL,1,30,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(24,2,'settings','Settings','ui',NULL,1,30,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(25,3,'settings','Settings','ui',NULL,1,30,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(26,1,'settings','Settings','ui',NULL,1,30,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(30,10,'properties','Properties','ui',NULL,1,10,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(31,8,'properties','Properties','ui',NULL,1,10,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(32,9,'properties','Properties','ui',NULL,1,10,'2026-03-25 12:43:45','2026-03-25 12:43:45'),(35,13,'dashboard','Dashboard','ui','{\"action\": \"load_content\", \"target_entry_key\": \"dashboard\"}',1,10,'2026-03-25 12:56:30','2026-03-25 12:56:30'),(36,13,'3d-viewer','3D Viewer','ui','{\"action\": \"load_content\", \"target_entry_key\": \"3d-viewer\"}',1,20,'2026-03-25 12:56:30','2026-03-25 12:56:30'),(37,13,'general','General','ui','{\"action\": \"load_content\", \"target_entry_key\": \"general\"}',1,30,'2026-03-25 12:56:30','2026-03-25 12:56:30');
/*!40000 ALTER TABLE `tool_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workspace_modules`
--

DROP TABLE IF EXISTS `workspace_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workspace_modules` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `module_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `module_type` enum('html','scene','dashboard','about','custom') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'html',
  `route_slug` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '100',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_workspace_modules_key` (`module_key`),
  UNIQUE KEY `uq_workspace_modules_slug` (`route_slug`),
  KEY `idx_workspace_modules_active_sort` (`is_active`,`sort_order`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workspace_modules`
--

LOCK TABLES `workspace_modules` WRITE;
/*!40000 ALTER TABLE `workspace_modules` DISABLE KEYS */;
INSERT INTO `workspace_modules` VALUES (1,'html','HTML View','html','html','Simple content page workspace',1,10,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(2,'cube','Cube View','scene','cube','3D scene workspace',1,20,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(3,'dashboard','Dashboard View','dashboard','dashboard','Dashboard workspace',1,30,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(4,'about','About','about','about','Project information workspace',1,40,'2026-03-25 12:43:27','2026-03-25 12:43:27'),(9,'help','Help','custom','help','Help workspace',1,50,'2026-03-25 12:56:00','2026-03-25 12:56:00');
/*!40000 ALTER TABLE `workspace_modules` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-25 11:56:18
