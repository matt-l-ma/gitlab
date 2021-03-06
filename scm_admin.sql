-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: scm_admin
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.12.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `git_group`
--

DROP TABLE IF EXISTS `git_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `git_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `git_id` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `owner_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_git_group_user` (`owner_id`),
  CONSTRAINT `FK_git_group_user` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `git_group`
--

LOCK TABLES `git_group` WRITE;
/*!40000 ALTER TABLE `git_group` DISABLE KEYS */;
INSERT INTO `git_group` VALUES (1,'Group1','/test/test/test1','another test group',3,1),(2,'Group2','/test/test/test2','create another repo',1,1),(3,'Group3','/test/test/test2','another test group',1,0),(6,'Group111','/test/test/test','create another ',1,0);
/*!40000 ALTER TABLE `git_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `git_repo`
--

DROP TABLE IF EXISTS `git_repo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `git_repo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `group_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_git_repo_git_group` (`group_id`),
  CONSTRAINT `FK_git_repo_git_group` FOREIGN KEY (`group_id`) REFERENCES `git_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `git_repo`
--

LOCK TABLES `git_repo` WRITE;
/*!40000 ALTER TABLE `git_repo` DISABLE KEYS */;
INSERT INTO `git_repo` VALUES (1,'Repo1','create another repo',1,1,1),(2,'Repo44','create another repo',1,0,4);
/*!40000 ALTER TABLE `git_repo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_access`
--

DROP TABLE IF EXISTS `group_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `access_type` enum('ReadOnly','ReadWrite') NOT NULL DEFAULT 'ReadOnly',
  `active` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_access`
--

LOCK TABLES `group_access` WRITE;
/*!40000 ALTER TABLE `group_access` DISABLE KEYS */;
INSERT INTO `group_access` VALUES (1,4,1,'',1);
/*!40000 ALTER TABLE `group_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repo_access`
--

DROP TABLE IF EXISTS `repo_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repo_access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `repo_id` int(11) NOT NULL,
  `access_type` enum('ReadOnly','ReadWrite') NOT NULL DEFAULT 'ReadOnly',
  `active` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repo_access`
--

LOCK TABLES `repo_access` WRITE;
/*!40000 ALTER TABLE `repo_access` DISABLE KEYS */;
INSERT INTO `repo_access` VALUES (1,3,1,'',1);
/*!40000 ALTER TABLE `repo_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (0,'ROLE_USER_ADMIN','User management account'),(1,'ROLE_GIT_ADMIN','Git management account'),(2,'ROLE_APPROVE','User has authority to approve');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_users`
--

DROP TABLE IF EXISTS `roles_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles_users` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `FK_role` (`role_id`),
  CONSTRAINT `FK_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `FK_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_users`
--

LOCK TABLES `roles_users` WRITE;
/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
INSERT INTO `roles_users` VALUES (2,0),(1,1),(1,2);
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('NewGroup','NewRepo','GroupAccess','RepoAccess') NOT NULL,
  `status` enum('Pending','Submit','Approve','Reject') NOT NULL,
  `content` text,
  `owner_id` int(11) NOT NULL,
  `approve_id` int(11) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `case_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_ticket_user_approve_id` (`approve_id`),
  KEY `FK_ticket_user_owner_id` (`owner_id`),
  CONSTRAINT `FK_ticket_user_approve_id` FOREIGN KEY (`approve_id`) REFERENCES `user` (`id`),
  CONSTRAINT `FK_ticket_user_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,'NewGroup','Approve','Name: Group1, Git Id: /test/test/test1, Description: another test group',3,1,'2018-01-27 19:25:55','2018-01-27 19:26:05',1),(2,'NewRepo','Approve','Name: Repo1, Group: Group1, Description: create another repo',1,1,'2018-01-27 19:26:54','2018-01-27 19:26:58',1),(3,'RepoAccess','Approve','User: Matt, Repo: Repo1, Access: Write',3,1,'2018-01-27 19:28:05','2018-01-27 19:28:08',1),(4,'GroupAccess','Approve','User: Leon, Group: Group1, Access: Write',4,1,'2018-01-27 23:15:09','2018-01-27 23:15:15',1),(5,'RepoAccess','Reject','User: Leon, Repo: Repo1, Access: Read',4,1,'2018-01-27 23:17:36','2018-01-27 23:17:39',2),(6,'NewRepo','Submit','Name: Repo44, Group: Group1, Description: create another repo',4,NULL,'2018-01-27 23:59:22','2018-01-27 23:59:27',2),(9,'NewGroup','Pending','Name: Group111, Git Id: /test/test/test, Description: create another ',1,NULL,'2018-01-28 20:10:48','2018-01-28 20:10:48',6);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(64) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'ivy','123','Shi Jing','ivy@163.com',1),(2,'admin','123','Admin','admin@163.com',1),(3,'matt','123','Matt','admin@111.com',1),(4,'leon','123','Leon','leon@163.com',1),(5,'chris','123','小鸡鸡','chris@163.com',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-28 20:16:50
