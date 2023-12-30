-- MySQL dump 10.13  Distrib 8.0.34, for macos13 (arm64)
--
-- Host: localhost    Database: patent_2022
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `g_application_in_progress`
--

DROP TABLE IF EXISTS `g_application_in_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `g_application_in_progress` (
  `table_number` int NOT NULL AUTO_INCREMENT,
  `applicant_id` int DEFAULT NULL,
  `patent_application_date` datetime DEFAULT NULL,
  `d_ipc` int DEFAULT NULL,
  `ipc_section` varchar(32) DEFAULT NULL,
  `patent_type` varchar(10) DEFAULT NULL,
  `patent_date` datetime DEFAULT NULL,
  `patent_title` text,
  `patent_abstract` text,
  `wipo_kind` varchar(3) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `Inventor_name1` varchar(20) DEFAULT NULL,
  `male_flag1` int DEFAULT '1',
  `Inventor_name2` varchar(20) DEFAULT NULL,
  `male_flag2` int DEFAULT '1',
  `Inventor_name3` varchar(20) DEFAULT NULL,
  `male_flag3` int DEFAULT '1',
  `Inventor_name4` varchar(20) DEFAULT NULL,
  `male_flag4` int DEFAULT '1',
  `Inventor_name5` varchar(20) DEFAULT NULL,
  `male_flag5` int DEFAULT '1',
  `Inventor_name6` varchar(20) DEFAULT NULL,
  `male_flag6` int DEFAULT '1',
  `Inventor_name7` varchar(20) DEFAULT NULL,
  `male_flag7` int DEFAULT '1',
  `Inventor_name8` varchar(20) DEFAULT NULL,
  `male_flag8` int DEFAULT '1',
  `Inventor_name9` varchar(20) DEFAULT NULL,
  `male_flag9` int DEFAULT '1',
  PRIMARY KEY (`table_number`),
  CONSTRAINT `g_application_in_progress_chk_1` CHECK (((`male_flag1` = 1) or (`male_flag1` = 0))),
  CONSTRAINT `g_application_in_progress_chk_10` CHECK (((`d_ipc` = 0) or (`d_ipc` = 1))),
  CONSTRAINT `g_application_in_progress_chk_11` CHECK (((`patent_type` = _utf8mb4'utility') or (`patent_type` = _utf8mb4'design') or (`patent_type` = _utf8mb4'plant') or (`patent_type` = _utf8mb4'reissue'))),
  CONSTRAINT `g_application_in_progress_chk_12` CHECK (((`status` = 1) or (`status` = 2) or (`status` = 3))),
  CONSTRAINT `g_application_in_progress_chk_2` CHECK (((`male_flag2` = 1) or (`male_flag2` = 0))),
  CONSTRAINT `g_application_in_progress_chk_3` CHECK (((`male_flag3` = 1) or (`male_flag3` = 0))),
  CONSTRAINT `g_application_in_progress_chk_4` CHECK (((`male_flag4` = 1) or (`male_flag4` = 0))),
  CONSTRAINT `g_application_in_progress_chk_5` CHECK (((`male_flag5` = 1) or (`male_flag5` = 0))),
  CONSTRAINT `g_application_in_progress_chk_6` CHECK (((`male_flag6` = 1) or (`male_flag6` = 0))),
  CONSTRAINT `g_application_in_progress_chk_7` CHECK (((`male_flag7` = 1) or (`male_flag7` = 0))),
  CONSTRAINT `g_application_in_progress_chk_8` CHECK (((`male_flag8` = 1) or (`male_flag8` = 0))),
  CONSTRAINT `g_application_in_progress_chk_9` CHECK (((`male_flag9` = 1) or (`male_flag9` = 0)))
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `g_application_in_progress`
--

LOCK TABLES `g_application_in_progress` WRITE;
/*!40000 ALTER TABLE `g_application_in_progress` DISABLE KEYS */;
INSERT INTO `g_application_in_progress` VALUES (9,1,'2023-12-29 10:32:33',1,'111','utility',NULL,'11','11','1',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,1,'2023-12-29 10:34:37',1,'11','plant',NULL,'111','11','1',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(11,1,'2023-12-29 10:38:15',0,'111','plant',NULL,'333','444','22',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(12,1,'2023-12-29 10:44:35',1,'11','design',NULL,'11','111','1',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(13,1,'2023-12-29 10:50:37',1,'2222','design',NULL,'111','111','22',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(14,1,'2023-12-29 10:54:43',0,'qq','design',NULL,'1111','111','111',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(15,1,'2023-12-29 10:55:59',0,'qq','utility',NULL,'qqq','qq','qqq',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(16,1,'2023-12-29 10:58:09',0,'1','utility',NULL,'11','11','11',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(17,1,'2023-12-29 11:03:57',0,'112222','utility',NULL,'111','111','1 1',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,1,'2023-12-29 11:24:33',0,'333','utility',NULL,'33','44','1',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,1,'2023-12-29 11:27:09',1,'1','utility',NULL,'title','abstract','2',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,1,'2023-12-29 11:55:53',0,'1','utility',NULL,'111','222','333',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,1,'2023-12-29 16:14:47',0,'11','design',NULL,'111','111','11',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(22,1,'2023-12-29 16:18:46',0,'11','design',NULL,'111','111','11',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(23,1,'2023-12-29 16:34:20',0,'idc','utility',NULL,'1','2','3',1,'Tracy Du',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(24,1,'2023-12-29 18:24:53',1,'geometry','utility',NULL,'1988','1988 is a nice tv show','11',1,'Tracy',0,'Franky',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `g_application_in_progress` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-30 12:05:29
