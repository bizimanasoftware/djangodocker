-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: db    Database: gloexdb
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.22.04.2

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
-- Table structure for table `accounts_customuser`
--

DROP TABLE IF EXISTS `accounts_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser`
--

LOCK TABLES `accounts_customuser` WRITE;
/*!40000 ALTER TABLE `accounts_customuser` DISABLE KEYS */;
INSERT INTO `accounts_customuser` VALUES (17,'pbkdf2_sha256$1000000$6vs6DL3XqosT3KRp7jldfB$pdrcayp+KNdL0zQQ+/uOa3zBEHHin0XZeWXHHnUrkUc=','2025-08-12 22:54:21.427752',1,'super','','','super@gloex.org',1,1,'2025-08-05 13:05:14.454687','ARTIST'),(24,'pbkdf2_sha256$1000000$0UyIpN6pnWwrnLs50jZ69P$HBTQurhMOmrZFASLI7nMnPzv4kH2LXp4HK1u9i+BIqY=','2025-08-07 17:57:54.633598',0,'arsene','','','arsene@gmail.com',0,1,'2025-08-07 17:47:53.653978','EMERGENCY'),(25,'pbkdf2_sha256$1000000$ofFdaP43yKhg4sOarAVCKC$IL777QBtrxgWF60V2MXDCxrlXcC4nxCjQIBbcwSnxEU=','2025-08-12 18:40:32.320763',1,'aman','','','aman@aman.org',1,1,'2025-08-07 19:52:52.000000','EMERGENCY'),(26,'pbkdf2_sha256$1000000$2NPm2qoYzcnuriiTV76nue$taKo7mm7b/cZJxvfIKEQUHeAqzLOTMbQS1tK8trP1Gg=','2025-08-07 21:43:44.954535',0,'laptop','','','laptop@gmail.com',0,1,'2025-08-07 21:43:41.562894','EMERGENCY'),(29,'pbkdf2_sha256$1000000$uClQ8RfShHJzHkzcF8KiYA$bHBNMePFPbM4A/n+7GvEgW/mYw0m22oXeXIklmIQHlM=','2025-08-10 07:47:54.433906',0,'gloex.org','','','info@gloex.org',0,1,'2025-08-09 14:38:02.399675','OTHER'),(30,'pbkdf2_sha256$1000000$iHMGOV0wiTyuRLz4EG07qW$PrFiwS3T8dOaELtzAWtzPUasBSdTgKHiPj/DFTrUBHo=','2025-08-10 16:29:31.478056',0,'support','','','support@gloex.org',0,1,'2025-08-10 16:29:27.738556','JOURNALIST'),(31,'pbkdf2_sha256$1000000$3Zr7tz6KKGVv41egONDUPn$n7o9LCsQtV4MILcJlRVsR3j5WEw0UeVlLIRMD97Y52s=','2025-08-12 15:44:09.000000',0,'longnameforever','','','suppor@gloex.org',0,1,'2025-08-12 15:44:05.000000','VOLLEYBALLER'),(32,'pbkdf2_sha256$1000000$wobh3sNSaKs8r410Fdx4rO$zsTOzViS4EAVuq0W79+/jpihYe68nDJVmdA8xr2VE/w=','2025-08-13 07:52:34.164437',0,'amano','','','amano@gmail.org',0,1,'2025-08-12 21:21:58.918021','ARTIST');
/*!40000 ALTER TABLE `accounts_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_groups`
--

DROP TABLE IF EXISTS `accounts_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq` (`customuser_id`,`group_id`),
  KEY `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_customuser__customuser_id_bc55088e_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_groups`
--

LOCK TABLES `accounts_customuser_groups` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_groups` DISABLE KEYS */;
INSERT INTO `accounts_customuser_groups` VALUES (13,25,2);
/*!40000 ALTER TABLE `accounts_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_user_permissions`
--

DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_customuser_id_permission_9632a709_uniq` (`customuser_id`,`permission_id`),
  KEY `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_customuser__customuser_id_0deaefae_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=403 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_user_permissions`
--

LOCK TABLES `accounts_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artists_account`
--

DROP TABLE IF EXISTS `artists_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists_account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_name` varchar(100) NOT NULL,
  `iban` varchar(34) NOT NULL,
  `balance` decimal(12,2) NOT NULL,
  `account_type` varchar(50) NOT NULL,
  `user_profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `iban` (`iban`),
  KEY `artists_account_user_profile_id_7ca699ef_fk_artists_u` (`user_profile_id`),
  CONSTRAINT `artists_account_user_profile_id_7ca699ef_fk_artists_u` FOREIGN KEY (`user_profile_id`) REFERENCES `artists_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists_account`
--

LOCK TABLES `artists_account` WRITE;
/*!40000 ALTER TABLE `artists_account` DISABLE KEYS */;
/*!40000 ALTER TABLE `artists_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artists_transaction`
--

DROP TABLE IF EXISTS `artists_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists_transaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `transaction_date` date NOT NULL,
  `category` varchar(100) NOT NULL,
  `channel` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `account_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `artists_transaction_account_id_a15f466f_fk_artists_account_id` (`account_id`),
  CONSTRAINT `artists_transaction_account_id_a15f466f_fk_artists_account_id` FOREIGN KEY (`account_id`) REFERENCES `artists_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists_transaction`
--

LOCK TABLES `artists_transaction` WRITE;
/*!40000 ALTER TABLE `artists_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `artists_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artists_userprofile`
--

DROP TABLE IF EXISTS `artists_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `country` varchar(100) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `artists_userprofile_user_id_db0f12e3_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists_userprofile`
--

LOCK TABLES `artists_userprofile` WRITE;
/*!40000 ALTER TABLE `artists_userprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `artists_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (4,'Agent'),(2,'Emergency'),(5,'Talent'),(3,'Volunteer');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (163,2,73),(164,2,74),(166,2,76),(167,2,77),(170,2,80),(171,2,81),(172,2,82),(175,2,85),(178,2,87),(179,2,88),(180,2,89),(181,2,90),(182,2,91),(183,2,92),(184,2,93),(185,2,94),(186,2,95),(176,2,96),(177,2,97);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_customuser'),(22,'Can change user',6,'change_customuser'),(23,'Can delete user',6,'delete_customuser'),(24,'Can view user',6,'view_customuser'),(25,'Can add wallet',7,'add_wallet'),(26,'Can change wallet',7,'change_wallet'),(27,'Can delete wallet',7,'delete_wallet'),(28,'Can view wallet',7,'view_wallet'),(29,'Can add transaction',8,'add_transaction'),(30,'Can change transaction',8,'change_transaction'),(31,'Can delete transaction',8,'delete_transaction'),(32,'Can view transaction',8,'view_transaction'),(33,'Can add thread',9,'add_thread'),(34,'Can change thread',9,'change_thread'),(35,'Can delete thread',9,'delete_thread'),(36,'Can view thread',9,'view_thread'),(37,'Can add message',10,'add_message'),(38,'Can change message',10,'change_message'),(39,'Can delete message',10,'delete_message'),(40,'Can view message',10,'view_message'),(41,'Can add chat permission',11,'add_chatpermission'),(42,'Can change chat permission',11,'change_chatpermission'),(43,'Can delete chat permission',11,'delete_chatpermission'),(44,'Can view chat permission',11,'view_chatpermission'),(45,'Can add chat message',12,'add_chatmessage'),(46,'Can change chat message',12,'change_chatmessage'),(47,'Can delete chat message',12,'delete_chatmessage'),(48,'Can view chat message',12,'view_chatmessage'),(49,'Can add profile',13,'add_profile'),(50,'Can change profile',13,'change_profile'),(51,'Can delete profile',13,'delete_profile'),(52,'Can view profile',13,'view_profile'),(53,'Can add profile gallery',14,'add_profilegallery'),(54,'Can change profile gallery',14,'change_profilegallery'),(55,'Can delete profile gallery',14,'delete_profilegallery'),(56,'Can view profile gallery',14,'view_profilegallery'),(57,'Can add sponsorship request',15,'add_sponsorshiprequest'),(58,'Can change sponsorship request',15,'change_sponsorshiprequest'),(59,'Can delete sponsorship request',15,'delete_sponsorshiprequest'),(60,'Can view sponsorship request',15,'view_sponsorshiprequest'),(61,'Can add Admin Chat Message',16,'add_adminchatmessage'),(62,'Can change Admin Chat Message',16,'change_adminchatmessage'),(63,'Can delete Admin Chat Message',16,'delete_adminchatmessage'),(64,'Can view Admin Chat Message',16,'view_adminchatmessage'),(65,'Can add user',17,'add_customuser'),(66,'Can change user',17,'change_customuser'),(67,'Can delete user',17,'delete_customuser'),(68,'Can view user',17,'view_customuser'),(69,'Can add donation',18,'add_donation'),(70,'Can change donation',18,'change_donation'),(71,'Can delete donation',18,'delete_donation'),(72,'Can view donation',18,'view_donation'),(73,'Can add emergency campaign',19,'add_emergencycampaign'),(74,'Can change emergency campaign',19,'change_emergencycampaign'),(75,'Can delete emergency campaign',19,'delete_emergencycampaign'),(76,'Can view emergency campaign',19,'view_emergencycampaign'),(77,'Can add campaign',20,'add_campaign'),(78,'Can change campaign',20,'change_campaign'),(79,'Can delete campaign',20,'delete_campaign'),(80,'Can view campaign',20,'view_campaign'),(81,'Can request an emergency campaign',19,'can_request_campaign'),(82,'Can add campaign image',21,'add_campaignimage'),(83,'Can change campaign image',21,'change_campaignimage'),(84,'Can delete campaign image',21,'delete_campaignimage'),(85,'Can view campaign image',21,'view_campaignimage'),(86,'Can add category',22,'add_category'),(87,'Can change category',22,'change_category'),(88,'Can delete category',22,'delete_category'),(89,'Can view category',22,'view_category'),(90,'Can add post',23,'add_post'),(91,'Can change post',23,'change_post'),(92,'Can delete post',23,'delete_post'),(93,'Can view post',23,'view_post'),(94,'Can add post image',24,'add_postimage'),(95,'Can change post image',24,'change_postimage'),(96,'Can delete post image',24,'delete_postimage'),(97,'Can view post image',24,'view_postimage'),(98,'Can add Received Email',25,'add_incomingemail'),(99,'Can change Received Email',25,'change_incomingemail'),(100,'Can delete Received Email',25,'delete_incomingemail'),(101,'Can view Received Email',25,'view_incomingemail'),(102,'Can add Email Draft',26,'add_emaildraft'),(103,'Can change Email Draft',26,'change_emaildraft'),(104,'Can delete Email Draft',26,'delete_emaildraft'),(105,'Can view Email Draft',26,'view_emaildraft'),(106,'Can add incoming attachment',27,'add_incomingattachment'),(107,'Can change incoming attachment',27,'change_incomingattachment'),(108,'Can delete incoming attachment',27,'delete_incomingattachment'),(109,'Can view incoming attachment',27,'view_incomingattachment'),(110,'Can add transaction',28,'add_transaction'),(111,'Can change transaction',28,'change_transaction'),(112,'Can delete transaction',28,'delete_transaction'),(113,'Can view transaction',28,'view_transaction'),(114,'Can add user profile',29,'add_userprofile'),(115,'Can change user profile',29,'change_userprofile'),(116,'Can delete user profile',29,'delete_userprofile'),(117,'Can view user profile',29,'view_userprofile'),(118,'Can add account',30,'add_account'),(119,'Can change account',30,'change_account'),(120,'Can delete account',30,'delete_account'),(121,'Can view account',30,'view_account');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_with_admin_adminchatmessage`
--

DROP TABLE IF EXISTS `chat_with_admin_adminchatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_with_admin_adminchatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sender_is_admin` tinyint(1) NOT NULL,
  `message` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read_by_user` tinyint(1) NOT NULL,
  `is_read_by_admin` tinyint(1) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `anonymous_sender_email` varchar(254) NOT NULL,
  `anonymous_sender_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_with_admin_admi_user_id_125accb4_fk_accounts_` (`user_id`),
  CONSTRAINT `chat_with_admin_admi_user_id_125accb4_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_with_admin_adminchatmessage`
--

LOCK TABLES `chat_with_admin_adminchatmessage` WRITE;
/*!40000 ALTER TABLE `chat_with_admin_adminchatmessage` DISABLE KEYS */;
INSERT INTO `chat_with_admin_adminchatmessage` VALUES (24,0,'Subject: Re: Increase google organic ranking & SEO\n\nHey team gloex.org,\r\n\r\nI would like to discuss SEO!\r\n\r\nI can help your website to get on first page of Google and increase the number of leads and sales you are getting from your website.\r\n\r\nMay I send you a quote & price list?\r\n\r\nBests Regards,\r\nAnkit\r\nBest AI SEO Company\r\nAccounts Manager\r\nwww.letsgetoptimize.com\r\nPhone No: +1 (949) 508-0277','2025-08-11 15:04:41.733243',1,0,NULL,'letsgetuoptimize@gmail.com','Ankit S'),(25,0,'Subject: Register gloex.org in the Google Search Index!\n\nHi,\r\n\r\nadd gloex.org to the Google Search Index so it can be displayed in search results. Visit now:\r\n\r\nhttps://SearchRegister.org/','2025-08-11 16:58:14.776771',1,0,NULL,'register@searchindex.net','Search Index'),(26,0,'Subject: Get more visitors for gloex.org\n\nHi,\r\n\r\nwe will help your website get a quick improvement in traffic.\r\n\r\nAdd gloex.org to SEODIRECTORY now:\r\n\r\nhttps://seodirectory.site','2025-08-13 06:41:25.060941',1,0,NULL,'elinor.binion85@gmail.com','Elinor Binion');
/*!40000 ALTER TABLE `chat_with_admin_adminchatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_with_admin_customuser`
--

DROP TABLE IF EXISTS `chat_with_admin_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_with_admin_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `can_access_chat` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_with_admin_customuser`
--

LOCK TABLES `chat_with_admin_customuser` WRITE;
/*!40000 ALTER TABLE `chat_with_admin_customuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_with_admin_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_with_admin_customuser_groups`
--

DROP TABLE IF EXISTS `chat_with_admin_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_with_admin_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_with_admin_customus_customuser_id_group_id_43cda1f9_uniq` (`customuser_id`,`group_id`),
  KEY `chat_with_admin_cust_group_id_3868264f_fk_auth_grou` (`group_id`),
  CONSTRAINT `chat_with_admin_cust_customuser_id_2b2cb87e_fk_chat_with` FOREIGN KEY (`customuser_id`) REFERENCES `chat_with_admin_customuser` (`id`),
  CONSTRAINT `chat_with_admin_cust_group_id_3868264f_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_with_admin_customuser_groups`
--

LOCK TABLES `chat_with_admin_customuser_groups` WRITE;
/*!40000 ALTER TABLE `chat_with_admin_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_with_admin_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_with_admin_customuser_user_permissions`
--

DROP TABLE IF EXISTS `chat_with_admin_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_with_admin_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_with_admin_customus_customuser_id_permission_3bb9fb7c_uniq` (`customuser_id`,`permission_id`),
  KEY `chat_with_admin_cust_permission_id_02b1413c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `chat_with_admin_cust_customuser_id_2553c73f_fk_chat_with` FOREIGN KEY (`customuser_id`) REFERENCES `chat_with_admin_customuser` (`id`),
  CONSTRAINT `chat_with_admin_cust_permission_id_02b1413c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_with_admin_customuser_user_permissions`
--

LOCK TABLES `chat_with_admin_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `chat_with_admin_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_with_admin_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=310 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (49,'2025-08-05 13:09:28.419082','10','[2025-08-05 11:57] foot: i miss you bby...',2,'[{\"changed\": {\"fields\": [\"Anonymous Sender Name\", \"Anonymous Sender Email\"]}}]',16,17),(50,'2025-08-05 13:10:44.901780','18','[2025-08-05 13:10] Admin: hell umuswaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...',1,'[{\"added\": {}}]',16,17),(51,'2025-08-05 19:11:35.320194','36','Sponsorship Deposit (Crypto) - 500.00000000 - Completed (ID: 892240fe-d68b-45bd-9e59-1e5cad6b7fb4)',2,'[{\"changed\": {\"fields\": [\"Fee\", \"Status\"]}}]',8,17),(52,'2025-08-05 22:43:27.764729','1','waterpollution',1,'[{\"added\": {}}]',19,17),(53,'2025-08-05 22:48:14.673192','1','waterpollution',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',19,17),(54,'2025-08-05 23:03:19.801947','5','super donated 5578.00 to waterpollution',3,'',18,17),(55,'2025-08-05 23:03:19.802071','3','super donated 7878787878.00 to waterpollution',3,'',18,17),(56,'2025-08-05 23:03:19.802155','2','super donated 9000.00 to waterpollution',3,'',18,17),(57,'2025-08-05 23:03:19.802233','1','super donated 600.00 to waterpollution',3,'',18,17),(58,'2025-08-06 07:08:49.815301','2','Emergency',1,'[{\"added\": {}}]',3,17),(59,'2025-08-06 07:25:47.236946','3','Volunteer',1,'[{\"added\": {}}]',3,17),(60,'2025-08-06 07:26:06.385936','4','Agent',1,'[{\"added\": {}}]',3,17),(61,'2025-08-06 09:07:32.080768','1','KIDNEY SURGERY',1,'[{\"added\": {}}]',20,17),(62,'2025-08-06 09:59:19.681396','3','Donation of 20.00 to KIDNEY SURGERY (COMPLETED)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',18,17),(63,'2025-08-06 09:59:32.714885','12','Donation of 500.00 to KIDNEY SURGERY (COMPLETED)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',18,17),(64,'2025-08-06 09:59:43.288643','9','Donation of 6000.00 to KIDNEY SURGERY (COMPLETED)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',18,17),(65,'2025-08-06 10:30:40.866345','14','Donation of 500.00 to KIDNEY SURGERY',2,'[{\"changed\": {\"fields\": [\"Is approved\", \"Status\"]}}]',18,17),(66,'2025-08-06 10:51:10.242685','1','Kidney SURGERY',1,'[{\"added\": {}}]',19,17),(67,'2025-08-06 19:36:34.611173','1','cancer therapy kenya',1,'[{\"added\": {}}, {\"added\": {\"name\": \"campaign image\", \"object\": \"Image for cancer therapy kenya\"}}]',19,17),(68,'2025-08-06 20:13:48.953308','2','robbery',1,'[{\"added\": {}}, {\"added\": {\"name\": \"campaign image\", \"object\": \"Image for robbery\"}}, {\"added\": {\"name\": \"campaign image\", \"object\": \"Image for robbery\"}}]',19,17),(69,'2025-08-06 20:23:29.776316','3','school fees',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(70,'2025-08-06 20:26:19.961817','9','name5\'s Wallet (Balance: 900000)',2,'[{\"changed\": {\"fields\": [\"Balance\"]}}]',7,17),(71,'2025-08-06 20:33:09.290956','1','name5 donated 9000.00 to school fees (completed)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',18,17),(72,'2025-08-06 20:33:33.041149','9','name5 donated 7000.00 to school fees (completed)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',18,17),(73,'2025-08-06 20:47:34.131047','10','name5 donated 300000.00 to robbery (completed)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',18,17),(74,'2025-08-06 21:43:04.607853','19','agent',2,'[{\"changed\": {\"fields\": [\"Groups\", \"User permissions\"]}}]',6,17),(75,'2025-08-07 10:36:46.450494','23','[2025-08-07 10:36] impuhwe: YES. IMPUHWE YOU ARE WELCOME , SO FOLLOW THE LINK ...',1,'[{\"added\": {}}]',16,17),(76,'2025-08-07 12:41:34.779080','21','apao',1,'[{\"added\": {}}]',6,17),(77,'2025-08-07 12:43:59.882311','21','apao',2,'[{\"changed\": {\"fields\": [\"Groups\", \"User permissions\"]}}]',6,17),(78,'2025-08-07 13:00:31.012239','23','papo',1,'[{\"added\": {}}]',6,17),(79,'2025-08-07 13:11:06.575424','23','papo',2,'[]',6,17),(80,'2025-08-07 13:13:52.350248','2','Emergency',2,'[]',3,17),(81,'2025-08-07 13:16:18.315535','2','Emergency',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,17),(82,'2025-08-07 13:17:30.716550','2','Emergency',2,'[]',3,17),(83,'2025-08-07 13:20:01.716700','23','papo',2,'[{\"changed\": {\"fields\": [\"Groups\", \"User permissions\"]}}]',6,17),(84,'2025-08-07 13:29:15.057260','22','wawa',2,'[]',6,17),(85,'2025-08-07 13:31:08.866899','2','Emergency',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,17),(86,'2025-08-07 13:31:47.119905','2','Emergency',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,17),(87,'2025-08-07 13:34:59.489084','19','agent',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Groups\", \"User permissions\"]}}]',6,17),(88,'2025-08-07 13:36:17.060352','19','agent',2,'[{\"changed\": {\"fields\": [\"Groups\", \"User permissions\"]}}]',6,17),(89,'2025-08-07 13:37:04.403139','19','agent',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\", \"User permissions\"]}}]',6,17),(90,'2025-08-07 13:39:27.133260','19','agent',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,17),(91,'2025-08-07 13:40:41.174843','19','agent',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\", \"Groups\"]}}]',6,17),(92,'2025-08-07 16:34:59.307532','62','Emergency Donation (Crypto) - 500.00000000 - Completed (ID: 0e462d1c-5056-460b-8391-a43c8b49aa54)',2,'[{\"changed\": {\"fields\": [\"Wallet\", \"Status\", \"Admin notes\", \"Admin payment instructions\"]}}]',8,17),(93,'2025-08-07 16:37:52.582930','61','Crypto Deposit - 30.00000000 - Completed (ID: 733546dd-b2b3-47ce-a28d-d547539aa985)',2,'[{\"changed\": {\"fields\": [\"Transaction type\", \"Status\"]}}]',8,17),(94,'2025-08-07 16:38:42.512995','59','Emergency Donation (Crypto) - 300.00000000 - Completed (ID: 08f608df-2a68-497e-8cfa-6a384ad907d7)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(95,'2025-08-07 16:41:45.963498','63','Sponsorship Deposit (Crypto) - 700.00000000 - Pending (ID: 142d415b-c0e4-4cd2-bb6b-151b6946ccc9)',3,'',8,17),(96,'2025-08-07 16:41:45.963735','62','Emergency Donation (Crypto) - 500.00000000 - Completed (ID: 0e462d1c-5056-460b-8391-a43c8b49aa54)',3,'',8,17),(97,'2025-08-07 16:41:45.963921','61','Crypto Deposit - 30.00000000 - Completed (ID: 733546dd-b2b3-47ce-a28d-d547539aa985)',3,'',8,17),(98,'2025-08-07 16:41:45.964123','60','Emergency Donation (Crypto) - 30.00000000 - Pending (ID: 4174e8d4-1b7d-4597-9d0f-0f05803a7854)',3,'',8,17),(99,'2025-08-07 16:41:45.964405','59','Emergency Donation (Crypto) - 300.00000000 - Completed (ID: 08f608df-2a68-497e-8cfa-6a384ad907d7)',3,'',8,17),(100,'2025-08-07 16:41:45.964619','58','Sponsorship Deposit (Crypto) - 4000.00000000 - Pending (ID: 27aacefa-00d9-446e-af08-b710330295d8)',3,'',8,17),(101,'2025-08-07 16:41:45.964903','57','Sponsorship Deposit (Manual) - 434.00000000 - Awaiting Admin Instructions (ID: 729207b9-1640-407f-8e4e-f50cb42b4511)',3,'',8,17),(102,'2025-08-07 16:41:45.965133','56','P2P Withdrawal - 58.00000000 - Pending (ID: 6edd27c5-668b-4c14-a131-62442bdb400b)',3,'',8,17),(103,'2025-08-07 16:41:45.965299','55','Crypto Withdrawal - 600.00000000 - Pending (ID: 2b3f0108-e0ef-4b40-a105-80ce3c173ede)',3,'',8,17),(104,'2025-08-07 16:41:45.965461','54','Internal Transfer (Received) - 500.00000000 - Completed (ID: f0249999-6b6b-42b5-bc35-fb8e154efc3a)',3,'',8,17),(105,'2025-08-07 16:41:45.965621','53','Internal Transfer (Sent) - 500.00000000 - Completed (ID: 0deb63e5-5035-4be6-836f-d969ea527801)',3,'',8,17),(106,'2025-08-07 16:41:45.965780','52','Crypto Deposit - 600.00000000 - Pending (ID: ac960547-abcd-46c3-a161-a01896e9fb0c)',3,'',8,17),(107,'2025-08-07 16:41:45.966058','51','P2P Deposit - 700.00000000 - Awaiting Admin Instructions (ID: a1ec6eb5-12b3-421d-8da8-d421b85122e5)',3,'',8,17),(108,'2025-08-07 16:41:45.966222','50','donation - 30.00000000 - Pending (ID: a90d40ff-f988-4ac3-a47c-0e7d2273bd67)',3,'',8,17),(109,'2025-08-07 16:41:45.966382','49','Sponsorship Deposit (Crypto) - 500.00000000 - Pending (ID: b4fc5577-cd30-43f6-ac43-dfbf87968b2e)',3,'',8,17),(110,'2025-08-07 16:41:45.966540','48','Sponsorship Deposit (Crypto) - 30.00000000 - Pending (ID: b58d7123-5a69-4e7e-9510-3d64b138778f)',3,'',8,17),(111,'2025-08-07 16:41:45.966696','47','Sponsorship Deposit (Crypto) - 15.00000000 - Pending (ID: ae48e68d-2a80-486a-ba70-eb4ec138c02d)',3,'',8,17),(112,'2025-08-07 16:41:45.966855','46','manual_credit - 7000.00000000 - Completed (ID: d7d45b00-8897-4d2d-9ead-04e4b0c4c627)',3,'',8,17),(113,'2025-08-07 16:41:45.967015','45','P2P Deposit - 400000.00000000 - Completed (ID: 42f02a12-4d8a-4223-8894-66a00b136d06)',3,'',8,17),(114,'2025-08-07 16:41:45.967176','44','Sponsorship Deposit (Crypto) - 300.00000000 - Pending (ID: 20904c0f-43b2-401a-a3f3-ef2c5503bff1)',3,'',8,17),(115,'2025-08-07 16:41:45.967334','43','donation_made - 300000.00000000 - Completed (ID: 810f2a5c-3e40-4663-b4e5-637f5056c622)',3,'',8,17),(116,'2025-08-07 16:41:45.967492','42','donation_made - 7000.00000000 - Completed (ID: dfcd7161-94ad-4b72-8bf4-1260413a1eba)',3,'',8,17),(117,'2025-08-07 16:41:45.967681','41','donation_made - 9000.00000000 - Completed (ID: cd6b4c51-e16e-4f9f-9c94-d4d3cd4a70fb)',3,'',8,17),(118,'2025-08-07 16:41:45.967845','40','Sponsorship Deposit (Crypto) - 700.00000000 - Pending (ID: 01f7cd8c-205e-48fc-a767-d204144908dd)',3,'',8,17),(119,'2025-08-07 16:41:45.968004','39','Sponsorship Deposit (Crypto) - 30.00000000 - Pending (ID: b435459e-f26a-4263-a25a-b180dbd87e59)',3,'',8,17),(120,'2025-08-07 16:41:45.968204','38','Sponsorship Deposit (Crypto) - 300.00000000 - Pending (ID: fe86f68e-9d5a-46a4-a678-1512ed2e0ecd)',3,'',8,17),(121,'2025-08-07 16:41:45.968374','37','Sponsorship Deposit (Manual) - 600.00000000 - Awaiting Proof of Payment (ID: 5b51e0e4-99a7-456d-ba73-eeae3b424655)',3,'',8,17),(122,'2025-08-07 16:41:45.968561','36','Sponsorship Deposit (Crypto) - 500.00000000 - Completed (ID: 892240fe-d68b-45bd-9e59-1e5cad6b7fb4)',3,'',8,17),(123,'2025-08-07 16:41:45.968723','35','Sponsorship Deposit (Crypto) - 19.00000000 - Pending (ID: 7a76dffb-c921-4cc9-a5a0-fe2b7c3ca5f8)',3,'',8,17),(124,'2025-08-07 16:41:45.968953','34','donation - 30.00000000 - Pending (ID: 175cb1d4-7a2b-443d-a420-235abf670b67)',3,'',8,17),(125,'2025-08-07 16:41:45.969119','33','Sponsorship Deposit (Crypto) - 19.00000000 - Pending (ID: 977acdb9-4744-4db4-85db-f5614366bdee)',3,'',8,17),(126,'2025-08-07 16:41:45.969279','32','Sponsorship Deposit (Crypto) - 30.00000000 - Pending (ID: 17e9b2ac-c090-4130-99b2-527017945fe2)',3,'',8,17),(127,'2025-08-07 16:41:45.969439','31','Sponsorship Deposit (Crypto) - 123.00000000 - Pending (ID: b9e41b65-6afa-438b-86fb-4f933c7612c2)',3,'',8,17),(128,'2025-08-07 16:41:45.969599','30','Sponsorship Deposit (Crypto) - 123.00000000 - Pending (ID: 978380f7-c3a4-41d2-b059-b6c113514c42)',3,'',8,17),(129,'2025-08-07 16:41:45.969756','29','donation - 50.00000000 - Pending (ID: 33a351b5-892c-47d8-83c7-a2fb6833a648)',3,'',8,17),(130,'2025-08-07 16:41:45.969913','28','Sponsorship Deposit (Manual) - 70000.00000000 - Awaiting Admin Instructions (ID: 758357b1-2cdc-400c-a0ce-f2f79683b695)',3,'',8,17),(131,'2025-08-07 16:41:45.970071','27','donation - 100.00000000 - Pending (ID: df82ce16-3b8f-4c37-ae9e-47d618d9d07b)',3,'',8,17),(132,'2025-08-07 16:41:45.970254','26','donation - 100.00000000 - Pending (ID: fb0da02e-b35b-4543-84fb-eb0838c6072e)',3,'',8,17),(133,'2025-08-07 16:41:45.970413','25','donation - 100.00000000 - Pending (ID: ee675ad4-837f-44a2-9e59-a95fc87288c0)',3,'',8,17),(134,'2025-08-07 16:41:45.970570','24','P2P Deposit - 678.00000000 - Awaiting Admin Instructions (ID: 00eb9b5c-e5ba-496b-9cdf-4e2b947754e8)',3,'',8,17),(135,'2025-08-07 16:41:45.970726','23','Crypto Deposit - 454.00000000 - Pending (ID: 01709aec-bbba-4318-89f2-d8b2c3bc3772)',3,'',8,17),(136,'2025-08-07 16:41:45.970883','22','Sponsorship Deposit (Manual) - 500.00000000 - Awaiting Admin Instructions (ID: 09910663-3083-4ab9-83e8-ce16dab630d4)',3,'',8,17),(137,'2025-08-07 16:41:45.971063','21','donation - 50.00000000 - Pending (ID: 9e616ecd-8643-4aa7-8a17-a5552e38b14f)',3,'',8,17),(138,'2025-08-07 16:41:45.971224','20','donation - 50000.00000000 - Pending (ID: a56e42b2-3f4e-4df0-9733-b2566685bc3e)',3,'',8,17),(139,'2025-08-07 16:41:45.971382','19','donation - 30.00000000 - Pending (ID: 527b5b4f-7bf8-4ac6-902e-086146671a2d)',3,'',8,17),(140,'2025-08-07 16:41:45.971538','18','donation - 30.00000000 - Pending (ID: f4d6b6ab-2288-4623-82bf-97ed11af71b1)',3,'',8,17),(141,'2025-08-07 16:41:45.971693','17','donation - 30.00000000 - Pending (ID: 3cb4ee5a-5279-4081-a4da-5016914fdbd6)',3,'',8,17),(142,'2025-08-07 16:41:45.971875','16','donation - 100.00000000 - Pending (ID: 62e81a20-7d59-4d72-8522-aaf001862c13)',3,'',8,17),(143,'2025-08-07 16:41:45.972056','15','donation - 50.00000000 - Pending (ID: 2fe21cda-5de0-4e19-827a-6e440acddd0a)',3,'',8,17),(144,'2025-08-07 16:41:45.972278','14','P2P Deposit - 500.00000000 - Awaiting Admin Instructions (ID: 426678ca-c5d9-4162-9a88-d7422502947f)',3,'',8,17),(145,'2025-08-07 16:41:45.972442','13','Crypto Deposit - 30.00000000 - Pending (ID: 9531c658-3339-4274-a101-c43774c698f7)',3,'',8,17),(146,'2025-08-07 16:41:45.972598','12','donation - 30.00000000 - Pending (ID: 4cd71526-41e7-483a-ba86-b95206a99f60)',3,'',8,17),(147,'2025-08-07 16:41:45.972755','11','P2P Deposit - 70.00000000 - Awaiting Admin Instructions (ID: 673cd93c-9d9b-4c41-917a-ea9b27b25299)',3,'',8,17),(148,'2025-08-07 16:41:45.972972','10','Crypto Deposit - 70.00000000 - Pending (ID: e8dccbaf-8ad1-4eda-a1eb-34a5392828fa)',3,'',8,17),(149,'2025-08-07 16:41:45.973130','9','donation - 30.00000000 - Pending (ID: 851fc7b2-1189-4376-975e-77e5b475bf63)',3,'',8,17),(150,'2025-08-07 16:41:45.973287','8','P2P Deposit - 300.00000000 - Awaiting Admin Instructions (ID: de7b2092-70b4-41f0-adcc-12e490e907fe)',3,'',8,17),(151,'2025-08-07 16:41:45.973444','7','donation - 50000.00000000 - Pending (ID: 674b530a-4fde-4789-9cae-f6bc5c96dbf9)',3,'',8,17),(152,'2025-08-07 16:41:45.973602','6','P2P Deposit - 400.00000000 - Awaiting Admin Instructions (ID: 1656cf04-4a93-4f28-a99d-0439fce98835)',3,'',8,17),(153,'2025-08-07 16:41:45.973760','5','P2P Deposit - 10.00000000 - Awaiting Admin Instructions (ID: 5eaa8876-a7c2-489f-aaf6-683892d26e49)',3,'',8,17),(154,'2025-08-07 16:41:45.973916','4','donation - 75.00000000 - Pending (ID: 2e436342-8e7c-4834-b2d3-e0f568e2a9aa)',3,'',8,17),(155,'2025-08-07 16:41:45.974072','3','donation - 75.00000000 - Pending (ID: 0e513317-8fa4-4ec5-a192-07cb7e75474e)',3,'',8,17),(156,'2025-08-07 16:41:45.974252','2','Crypto Deposit - 30.00000000 - Pending (ID: 7daec726-d0c4-4dc4-a703-687ef57a0035)',3,'',8,17),(157,'2025-08-07 16:41:45.974412','1','donation - 90.00000000 - Pending (ID: c9d0a529-2f46-4826-8424-2613e25e8d49)',3,'',8,17),(158,'2025-08-07 16:42:42.848121','23','papo\'s Wallet (Balance: 0E-8)',3,'',7,17),(159,'2025-08-07 16:42:42.848282','22','wawa\'s Wallet (Balance: 0E-8)',3,'',7,17),(160,'2025-08-07 16:42:42.848367','21','apao\'s Wallet (Balance: 0E-8)',3,'',7,17),(161,'2025-08-07 16:42:42.848446','20','impuhwe\'s Wallet (Balance: 400000.00000000)',3,'',7,17),(162,'2025-08-07 16:42:42.848522','19','agent\'s Wallet (Balance: 5142.00000000)',3,'',7,17),(163,'2025-08-07 16:42:42.848599','18','ababa\'s Wallet (Balance: 0E-8)',3,'',7,17),(164,'2025-08-07 16:42:42.848675','17','super\'s Wallet (Balance: 0E-8)',3,'',7,17),(165,'2025-08-07 16:42:42.848749','16','safari\'s Wallet (Balance: 0E-8)',3,'',7,17),(166,'2025-08-07 16:42:42.848855','15','foot\'s Wallet (Balance: 0E-8)',3,'',7,17),(167,'2025-08-07 16:42:42.848932','14','wewe\'s Wallet (Balance: 0E-8)',3,'',7,17),(168,'2025-08-07 16:42:42.849006','13','name10\'s Wallet (Balance: 0E-8)',3,'',7,17),(169,'2025-08-07 16:42:42.849077','12','name9\'s Wallet (Balance: 0E-8)',3,'',7,17),(170,'2025-08-07 16:42:42.849150','11','name7\'s Wallet (Balance: 0E-8)',3,'',7,17),(171,'2025-08-07 16:42:42.849223','10','name6\'s Wallet (Balance: 0E-8)',3,'',7,17),(172,'2025-08-07 16:42:42.849296','9','name5\'s Wallet (Balance: 583500.00000000)',3,'',7,17),(173,'2025-08-07 16:42:42.849369','8','name3\'s Wallet (Balance: 0E-8)',3,'',7,17),(174,'2025-08-07 16:42:42.849441','7','name2\'s Wallet (Balance: 0E-8)',3,'',7,17),(175,'2025-08-07 16:42:42.849513','6','name1\'s Wallet (Balance: 0E-8)',3,'',7,17),(176,'2025-08-07 16:42:42.849587','5','igikombe\'s Wallet (Balance: 0E-8)',3,'',7,17),(177,'2025-08-07 16:42:42.849659','4','admin\'s Wallet (Balance: 0E-8)',3,'',7,17),(178,'2025-08-07 16:42:42.849733','3','irido\'s Wallet (Balance: 500.00000000)',3,'',7,17),(179,'2025-08-07 16:42:42.849806','2','manager\'s Wallet (Balance: 0E-8)',3,'',7,17),(180,'2025-08-07 16:42:42.849879','1','arsene\'s Wallet (Balance: 0E-8)',3,'',7,17),(181,'2025-08-07 16:43:54.463704','18','ababa',3,'',6,17),(182,'2025-08-07 16:43:54.463805','4','admin',3,'',6,17),(183,'2025-08-07 16:43:54.463873','19','agent',3,'',6,17),(184,'2025-08-07 16:43:54.463936','21','apao',3,'',6,17),(185,'2025-08-07 16:43:54.463999','1','arsene',3,'',6,17),(186,'2025-08-07 16:43:54.464062','15','foot',3,'',6,17),(187,'2025-08-07 16:43:54.464123','5','igikombe',3,'',6,17),(188,'2025-08-07 16:43:54.464271','20','impuhwe',3,'',6,17),(189,'2025-08-07 16:43:54.464337','3','irido',3,'',6,17),(190,'2025-08-07 16:43:54.464400','2','manager',3,'',6,17),(191,'2025-08-07 16:43:54.464462','6','name1',3,'',6,17),(192,'2025-08-07 16:43:54.464524','13','name10',3,'',6,17),(193,'2025-08-07 16:43:54.464585','7','name2',3,'',6,17),(194,'2025-08-07 16:43:54.464646','8','name3',3,'',6,17),(195,'2025-08-07 16:43:54.464706','9','name5',3,'',6,17),(196,'2025-08-07 16:43:54.464768','10','name6',3,'',6,17),(197,'2025-08-07 16:43:54.464858','11','name7',3,'',6,17),(198,'2025-08-07 16:43:54.464921','12','name9',3,'',6,17),(199,'2025-08-07 16:43:54.464983','23','papo',3,'',6,17),(200,'2025-08-07 16:43:54.465045','16','safari',3,'',6,17),(201,'2025-08-07 16:43:54.465105','22','wawa',3,'',6,17),(202,'2025-08-07 16:43:54.465167','14','wewe',3,'',6,17),(203,'2025-08-07 16:44:59.500125','1','Talent team',3,'',3,17),(204,'2025-08-07 16:45:24.966709','5','Talent',1,'[{\"added\": {}}]',3,17),(205,'2025-08-07 16:46:02.924367','14','[2025-08-05 12:50] patric (agent@gmail.com): Subject: i need monew\n\nsjhwddudwdwcdcwcdhwwswfyfyu...',3,'',16,17),(206,'2025-08-07 16:46:02.924500','17','[2025-08-05 13:01] Bbbbbbb (arsenbbbbbbe@gmail.com): Subject: Dbddbdbdb\n\nNsbsbsbdbdbxbdmsmdvdvdbdbxb...',3,'',16,17),(207,'2025-08-07 16:46:02.924608','19','[2025-08-05 13:22] Patrick (patrick@gmail.com): Subject: Not Patrick\n\nHshsjdjdjjdjd in the morning...',3,'',16,17),(208,'2025-08-07 16:46:02.924710','20','[2025-08-05 13:32] wewe (iro@gloex.org): Subject: hchchhvkvjvkh\n\nfuigugncnhchjc,cjhgik...',3,'',16,17),(209,'2025-08-07 16:46:02.924842','21','[2025-08-07 06:41] Talent team (arsene@gmail.com): Subject: Not Patrick\n\nStud finder and to transfer ...',3,'',16,17),(210,'2025-08-07 16:46:40.247930','3','school fees',3,'',19,17),(211,'2025-08-07 16:46:40.248025','2','robbery',3,'',19,17),(212,'2025-08-07 16:46:40.248088','1','cancer therapy kenya',3,'',19,17),(213,'2025-08-07 16:59:52.495181','4','team',1,'[{\"added\": {}}, {\"added\": {\"name\": \"campaign image\", \"object\": \"Image for team\"}}]',19,17),(214,'2025-08-07 17:04:46.969293','64','Emergency Donation (Crypto) - 700.00000000 - Completed (ID: c84121fb-ab45-47af-8186-349d6a192d31)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(215,'2025-08-07 17:06:43.889964','5','water',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(216,'2025-08-07 17:47:56.790255','24','arsene',1,'[{\"added\": {}}]',6,17),(217,'2025-08-07 17:48:50.546738','5','water',2,'[{\"changed\": {\"fields\": [\"Recipient\"]}}]',19,17),(218,'2025-08-07 17:50:47.831547','66','Emergency Donation (Crypto) - 399.00000000 - Pending (ID: ebcd4c98-2ffd-43a1-adcb-7fa80fc717e5)',2,'[{\"changed\": {\"fields\": [\"Wallet\", \"Fee\"]}}]',8,17),(219,'2025-08-07 17:51:23.858292','66','Emergency Donation (Crypto) - 399.00000000 - Completed (ID: ebcd4c98-2ffd-43a1-adcb-7fa80fc717e5)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(220,'2025-08-07 18:07:25.001250','6','accident',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(221,'2025-08-07 18:11:54.745791','68','Emergency Donation (Crypto) - 500.00000000 - Completed (ID: 2b0b9404-50c0-46e6-97e7-edaf6464c7bf)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(222,'2025-08-07 18:13:26.570385','68','Emergency Donation (Crypto) - 500.00000000 - Completed (ID: 2b0b9404-50c0-46e6-97e7-edaf6464c7bf)',2,'[{\"changed\": {\"fields\": [\"Wallet\"]}}]',8,17),(223,'2025-08-07 18:21:11.176233','68','Emergency Donation (Crypto) - 500.00000000 - Failed (ID: 2b0b9404-50c0-46e6-97e7-edaf6464c7bf)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(224,'2025-08-07 18:22:09.666550','68','Emergency Donation (Crypto) - 500.00000000 - Failed (ID: 2b0b9404-50c0-46e6-97e7-edaf6464c7bf)',2,'[]',8,17),(225,'2025-08-07 18:46:07.221235','68','Emergency Donation (Crypto) - 500.00000000 - Completed (ID: 2b0b9404-50c0-46e6-97e7-edaf6464c7bf)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(226,'2025-08-07 18:48:47.121724','6','accident',2,'[{\"changed\": {\"fields\": [\"Current amount\"]}}]',19,17),(227,'2025-08-07 18:49:30.847480','6','accident',2,'[{\"changed\": {\"fields\": [\"Current amount\"]}}]',19,17),(228,'2025-08-07 19:11:20.407170','6','accident',3,'',19,17),(229,'2025-08-07 19:17:18.239598','7','disaster',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(230,'2025-08-07 19:17:39.475406','8','ROBERRY',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(231,'2025-08-07 19:18:02.170526','9','DISEASE',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(232,'2025-08-07 19:18:23.078674','10','GGKSDKsd',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',19,17),(233,'2025-08-07 19:24:00.861434','11','hgugudu',2,'[{\"changed\": {\"fields\": [\"Current amount\"]}}]',19,17),(234,'2025-08-07 19:24:37.041422','11','hgugudu',2,'[{\"changed\": {\"fields\": [\"Current amount\", \"Status\"]}}]',19,17),(235,'2025-08-07 19:48:34.416268','2','Emergency',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,17),(236,'2025-08-07 19:50:09.631492','25','aman',2,'[{\"changed\": {\"fields\": [\"Groups\", \"Date joined\"]}}]',6,17),(237,'2025-08-07 19:52:55.658548','25','aman',2,'[{\"changed\": {\"fields\": [\"Superuser status\", \"Groups\", \"Date joined\"]}}]',6,17),(238,'2025-08-07 20:01:46.354368','11','hgugudu',3,'',19,17),(239,'2025-08-07 20:01:46.354501','10','GGKSDKsd',3,'',19,17),(240,'2025-08-07 20:01:46.354572','9','DISEASE',3,'',19,17),(241,'2025-08-07 20:01:46.354635','8','ROBERRY',3,'',19,17),(242,'2025-08-07 20:01:46.354696','7','disaster',3,'',19,17),(243,'2025-08-07 20:01:46.354758','5','water',3,'',19,17),(244,'2025-08-07 20:01:46.354817','4','team',3,'',19,17),(245,'2025-08-07 20:02:14.640625','25','aman\'s Profile',3,'',13,17),(246,'2025-08-07 20:02:14.640832','24','arsene\'s Profile',3,'',13,17),(247,'2025-08-07 20:02:14.640925','17','super\'s Profile',3,'',13,17),(248,'2025-08-08 05:52:02.991074','1','Announcements',1,'[{\"added\": {}}]',22,17),(249,'2025-08-08 05:52:22.568735','2','Updates',1,'[{\"added\": {}}]',22,17),(250,'2025-08-08 05:52:37.772489','3','Events',1,'[{\"added\": {}}]',22,17),(251,'2025-08-08 05:53:04.516753','4','Opportunities',1,'[{\"added\": {}}]',22,17),(252,'2025-08-08 06:15:25.415831','1','WE HAVE LAUNCHED EMERGENCY AID SYSTEM',1,'[{\"added\": {}}]',23,17),(253,'2025-08-08 06:30:06.337241','1','WE HAVE LAUNCHED EMERGENCY AID SYSTEM',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',23,17),(254,'2025-08-08 06:44:11.769421','2','WE ARE SO EXCITED',1,'[{\"added\": {}}]',23,17),(255,'2025-08-08 07:22:15.902879','3','WE GO',1,'[{\"added\": {}}, {\"added\": {\"name\": \"post image\", \"object\": \"Image for post: WE GO\"}}, {\"added\": {\"name\": \"post image\", \"object\": \"Image for post: WE GO\"}}]',23,17),(256,'2025-08-08 08:14:31.333528','2','Emergency',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,17),(257,'2025-08-08 08:16:06.406875','25','aman',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Groups\"]}}]',6,17),(258,'2025-08-08 08:17:59.131957','25','aman',2,'[{\"changed\": {\"fields\": [\"Superuser status\", \"Groups\"]}}]',6,17),(259,'2025-08-08 08:20:44.386648','2','Emergency',2,'[]',3,17),(260,'2025-08-08 08:21:52.062468','25','aman',2,'[{\"changed\": {\"fields\": [\"Superuser status\", \"Groups\"]}}]',6,17),(261,'2025-08-08 13:18:32.706186','27','ihene',1,'[{\"added\": {}}]',6,25),(262,'2025-08-08 13:21:04.289706','27','Image for ihene uploaded at 2025-08-08',1,'[{\"added\": {}}]',14,25),(263,'2025-08-08 15:49:17.410307','28','ihene\'s Profile',3,'',13,17),(264,'2025-08-08 15:49:17.410442','27','laptop\'s Profile',3,'',13,17),(265,'2025-08-08 15:49:17.410520','26','aman\'s Profile',3,'',13,17),(266,'2025-08-08 18:14:59.503483','6','Welcome  at Gloex.org',1,'[{\"added\": {}}]',23,17),(267,'2025-08-08 18:19:14.373951','6','Welcome  at Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\", \"Status\"]}}]',23,17),(268,'2025-08-08 18:51:31.240681','7','LAUNCHING Gloex.org',1,'[{\"added\": {}}]',23,17),(269,'2025-08-08 19:01:55.225743','7','LAUNCHING Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(270,'2025-08-08 19:04:22.331044','7','LAUNCHING Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(271,'2025-08-08 19:06:48.652805','7','LAUNCHING Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(272,'2025-08-08 19:11:25.154858','7','LAUNCHING Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(273,'2025-08-08 19:51:02.046566','7','LAUNCHING Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(274,'2025-08-08 19:53:06.386454','7','LAUNCHING Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(275,'2025-08-08 19:56:44.885746','6','Welcome  at Gloex.org',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(276,'2025-08-08 20:00:59.264861','8','THIS IS YOUR TIME',1,'[{\"added\": {}}]',23,17),(277,'2025-08-08 20:02:12.834152','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',23,17),(278,'2025-08-08 20:10:07.917801','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\", \"Image\"]}}]',23,17),(279,'2025-08-08 20:14:36.109082','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(280,'2025-08-08 20:18:54.636010','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Title color\", \"Underline title\"]}}]',23,17),(281,'2025-08-08 20:19:14.765680','6','Welcome  at Gloex.org',3,'',23,17),(282,'2025-08-08 20:19:14.765780','7','LAUNCHING Gloex.org',3,'',23,17),(283,'2025-08-08 20:22:46.952122','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(284,'2025-08-08 20:37:08.161016','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(285,'2025-08-08 20:40:00.905542','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(286,'2025-08-08 20:44:43.983185','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(287,'2025-08-08 20:44:46.918968','8','THIS IS YOUR TIME',2,'[]',23,17),(288,'2025-08-08 20:45:38.543010','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',23,17),(289,'2025-08-09 14:23:39.932575','28','Image for Aman_Amanda uploaded at 2025-08-09',1,'[{\"added\": {}}]',14,17),(290,'2025-08-09 14:38:05.588417','29','gloex.org',1,'[{\"added\": {}}]',6,17),(291,'2025-08-09 14:39:36.015680','14','General Donation',2,'[{\"changed\": {\"fields\": [\"Title\", \"Slug\", \"Creator\", \"Recipient\", \"Current amount\", \"Status\"]}}]',19,17),(292,'2025-08-09 18:31:17.332700','1','Draft for: infogloex@proton.me | Subject: Congratulations',1,'[{\"added\": {}}]',26,17),(293,'2025-08-09 21:10:00.499933','1','Draft for: infogloex@proton.me | Subject: Congratulations',2,'[]',26,17),(294,'2025-08-10 08:19:08.483042','30','Aman_Amanda\'s Profile',3,'',13,17),(295,'2025-08-10 08:19:08.483155','29','super\'s Profile',3,'',13,17),(296,'2025-08-10 09:52:14.428030','14','General Donation',2,'[{\"changed\": {\"fields\": [\"Description\", \"Image\"]}}]',19,17),(297,'2025-08-10 09:57:29.579406','14','General Donation',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',19,17),(298,'2025-08-10 09:59:15.126689','31','gloex.org\'s Profile',2,'[{\"changed\": {\"fields\": [\"Bio\"]}}]',13,17),(299,'2025-08-10 10:14:32.595823','5','competitions',1,'[{\"added\": {}}]',22,17),(300,'2025-08-10 10:15:19.801895','6','projects',1,'[{\"added\": {}}]',22,17),(301,'2025-08-10 13:38:50.378666','14','General Donation',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',19,17),(302,'2025-08-10 13:39:45.166755','31','gloex.org\'s Profile',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',13,17),(303,'2025-08-10 13:41:36.499881','8','THIS IS YOUR TIME',2,'[{\"changed\": {\"fields\": [\"Body\", \"Image\"]}}]',23,17),(304,'2025-08-10 21:40:28.999823','28','Aman_Amanda',3,'',6,17),(305,'2025-08-10 21:40:29.000011','27','ihene',3,'',6,17),(306,'2025-08-10 23:10:52.468838','86','Sponsorship Deposit (Manual) - 300.00000000 - Completed (ID: c40c1c46-9731-45e4-8def-a8192fdf6924)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(307,'2025-08-10 23:11:56.395445','85','Sponsorship Deposit (Crypto) - 300.00000000 - Completed (ID: 9848e435-1076-40fe-beab-24398f14fe64)',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,17),(308,'2025-08-12 22:49:53.021590','31','longnameforever',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',6,17),(309,'2025-08-12 23:02:39.250190','33','super\'s Profile',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',13,17);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','customuser'),(1,'admin','logentry'),(30,'artists','account'),(28,'artists','transaction'),(29,'artists','userprofile'),(3,'auth','group'),(2,'auth','permission'),(16,'chat_with_admin','adminchatmessage'),(17,'chat_with_admin','customuser'),(4,'contenttypes','contenttype'),(26,'emails','emaildraft'),(27,'emails','incomingattachment'),(25,'emails','incomingemail'),(20,'emergencies','campaign'),(21,'emergencies','campaignimage'),(18,'emergencies','donation'),(19,'emergencies','emergencycampaign'),(12,'messaging','chatmessage'),(11,'messaging','chatpermission'),(10,'messaging','message'),(9,'messaging','thread'),(13,'profiles','profile'),(14,'profiles','profilegallery'),(15,'profiles','sponsorshiprequest'),(5,'sessions','session'),(22,'updates','category'),(23,'updates','post'),(24,'updates','postimage'),(8,'wallet','transaction'),(7,'wallet','wallet');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-08-02 18:24:15.466863'),(2,'contenttypes','0002_remove_content_type_name','2025-08-02 18:24:17.714944'),(3,'auth','0001_initial','2025-08-02 18:24:23.906507'),(4,'auth','0002_alter_permission_name_max_length','2025-08-02 18:24:25.349130'),(5,'auth','0003_alter_user_email_max_length','2025-08-02 18:24:25.448687'),(6,'auth','0004_alter_user_username_opts','2025-08-02 18:24:25.552203'),(7,'auth','0005_alter_user_last_login_null','2025-08-02 18:24:25.724703'),(8,'auth','0006_require_contenttypes_0002','2025-08-02 18:24:25.832027'),(9,'auth','0007_alter_validators_add_error_messages','2025-08-02 18:24:26.045976'),(10,'auth','0008_alter_user_username_max_length','2025-08-02 18:24:26.235143'),(11,'auth','0009_alter_user_last_name_max_length','2025-08-02 18:24:26.356052'),(12,'auth','0010_alter_group_name_max_length','2025-08-02 18:24:26.743335'),(13,'auth','0011_update_proxy_permissions','2025-08-02 18:24:27.011203'),(14,'auth','0012_alter_user_first_name_max_length','2025-08-02 18:24:27.155581'),(15,'accounts','0001_initial','2025-08-02 18:24:35.228774'),(16,'accounts','0002_alter_customuser_user_type','2025-08-02 18:24:35.305610'),(17,'accounts','0003_alter_customuser_user_type','2025-08-02 18:24:35.396126'),(18,'admin','0001_initial','2025-08-02 18:24:38.153714'),(19,'admin','0002_logentry_remove_auto_add','2025-08-02 18:24:38.235450'),(20,'admin','0003_logentry_add_action_flag_choices','2025-08-02 18:24:38.358638'),(22,'sessions','0001_initial','2025-08-02 18:24:45.587307'),(23,'wallet','0001_initial','2025-08-02 18:24:52.434005'),(24,'messaging','0002_message_is_deleted_thread_is_active_and_more','2025-08-02 20:24:22.129088'),(25,'messaging','0003_remove_message_sender_remove_message_thread_and_more','2025-08-02 21:32:07.812519'),(26,'messaging','0001_initial','2025-08-03 07:57:21.206417'),(27,'profiles','0001_initial','2025-08-04 08:34:49.624901'),(28,'profiles','0002_profile_delete_userprofile','2025-08-04 08:34:51.739108'),(29,'profiles','0003_remove_profile_birth_date_remove_profile_location_and_more','2025-08-04 08:35:00.666596'),(30,'profiles','0004_remove_profile_intro_video_and_more','2025-08-04 10:35:26.752772'),(31,'chat_with_admin','0001_initial','2025-08-05 10:18:31.306636'),(32,'chat_with_admin','0002_customuser','2025-08-05 11:55:57.671856'),(33,'chat_with_admin','0003_adminchatmessage_anonymous_sender_email_and_more','2025-08-05 12:38:26.506734'),(34,'wallet','0002_transaction_sponsor_transaction_sponsor_guest_email_and_more','2025-08-05 16:26:12.108254'),(35,'wallet','0003_alter_transaction_transaction_type','2025-08-05 18:09:05.810546'),(46,'emergencies','0001_initial','2025-08-06 18:53:10.606430'),(47,'emergencies','0002_alter_donation_donor','2025-08-07 14:17:21.766664'),(48,'emergencies','0003_alter_emergencycampaign_options_and_more','2025-08-07 15:53:51.545547'),(49,'wallet','0004_transaction_campaign_and_more','2025-08-07 15:55:05.469336'),(50,'emergencies','0004_emergencycampaign_recipient_and_more','2025-08-07 17:44:18.244393'),(51,'updates','0001_initial','2025-08-08 05:24:41.352392'),(52,'updates','0002_alter_post_attachment_postimage','2025-08-08 07:01:48.637505'),(53,'emails','0001_initial','2025-08-09 18:20:30.411435'),(54,'emails','0002_incomingattachment','2025-08-09 21:05:43.192660');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3a58ojqexpyg8hhawjgajfb91jmlv2qg','.eJxVjEEOwiAQRe_C2hCGFhhduvcMhGEGqZo2Ke3KeHfbpAvd_vfef6uY1qXGtckcB1YXBUGdfkdK-SnjTviRxvuk8zQu80B6V_RBm75NLK_r4f4d1NTqVltGAsoWmYWDQXEgoYQevTHO9YDBA1mwgIAiJVPZaIfdmQmQvVGfLwQ_N7c:1ukkSc:AlbZ98vw0fodABNlU24hYkE_Ad2pO5pBUkhyqlNP-54','2025-08-23 14:22:14.398918'),('5qmb7z7m76wa1anmilh4fzw941tq1xl0','.eJxVjMEOwiAQBf-FsyFAFygevfcbCCyLVA0kpT0Z_9026UGvb2bem_mwrcVvnRY_J3Zl0rHL7xgDPqkeJD1CvTeOra7LHPmh8JN2PrVEr9vp_h2U0MteaxOkVTa60UmRyRmJQiNESDRYA0mOARKCJtwZoRqsILQ5i6yyIQHs8wX_bjhH:1ujQg0:MUtoLjXKHUHuSOJMGfuh-wDir-dpp6lbQ87oCsuRo3k','2025-08-19 23:02:36.427813'),('6431p16yflo7zqkmb9b17rvlux30c9zc','.eJxVjMEOwiAQRP-FsyFQLO169O43kGV3laqBpLQn47-XJj3obWbezHxUwHVJYa0yh4nVRYE6_WYR6SV5B_zE_CiaSl7mKeq9og9a9a2wvK9H9-8gYU1t3TlH2IE3RNAkD2Jdc3YUkWEkFgQD0ZyxZwSL9k7ijWfrBSlGBvXdAO0kOL8:1ujlEA:_nUnraiQxg3ciAKWydnRxhGyfvAQtA0qECMvGwFBuIM','2025-08-20 20:59:14.118098'),('6uozjze8l520v7124vtgwmr2tm8r2fda','.eJxVjMEOwiAQRP-FsyFQLO169O43kGV3laqBpLQn47-XJj3obWbezHxUwHVJYa0yh4nVRYE6_WYR6SV5B_zE_CiaSl7mKeq9og9a9a2wvK9H9-8gYU1t3TlH2IE3RNAkD2Jdc3YUkWEkFgQD0ZyxZwSL9k7ijWfrBSlGBvXdAO0kOL8:1ujE3p:mCVfUy0SjA_gcyorSGpgfVBaL0IZ_liwtdNae2U4HnY','2025-08-19 09:34:21.435144'),('9iy99vbenm03yoryfguhru3kkkupkdjr','.eJxVjDsOwjAQBe_iGlnEv8WU9JzBWu-ucQA5UpxUiLtDpBTQvpl5L5VwXWpau8xpZHVWTh1-t4z0kLYBvmO7TZqmtsxj1puid9r1dWJ5Xnb376Bir9-6iAg7GEz2fAQsmQNhNEOJhFQ82cLiwbAjE0ggWovFBnQuAjgwJ_X-ACgJONY:1uiwWV:nEgKcJXg-Bn0hwn4mXCRYa3iRAX3iBcLJDf9itbQYi4','2025-08-18 14:50:47.763171'),('a0if2xqmn226ci12kaoa4ika3p51v5q7','.eJxVjMsOwiAQRf-FtSF0eLt07zeQgQGpGkhKuzL-uzbpQrf3nHNfLOC21rCNvISZ2JmBZqffMWJ65LYTumO7dZ56W5c58l3hBx382ik_L4f7d1Bx1G8dk8reCJti8t6hsVZKPZUJyYIplFEbT84IqdEVj2CTkkoAAOWoHDj2_gALBTe6:1ulm8B:RgeMYX4z2vBUy-auWG6zYvmbA9xQtzU-17HnML7IfIM','2025-08-26 10:21:23.103145'),('as9ylhwdnedoin4q6be8212urnpqvjby','.eJxVjEEOwiAQRe_C2hCGFhhduvcMhGEGqZo2Ke3KeHfbpAvd_vfef6uY1qXGtckcB1YXBUGdfkdK-SnjTviRxvuk8zQu80B6V_RBm75NLK_r4f4d1NTqVltGAsoWmYWDQXEgoYQevTHO9YDBA1mwgIAiJVPZaIfdmQmQvVGfLwQ_N7c:1ukRZu:2TfO8L0PkPFuS14mvRGslFNmFs7S_8rJbhvbPpalhMM','2025-08-22 18:12:30.727526'),('b0ji8dahr7h42oridvrnvezy9m9ip2xf','.eJxVjDsOwjAQBe_iGllrx_GHkp4zWOvdNQmgRIqTCnF3iJQC2jcz76UybuuQtyZLHlmdlbHq9DsWpIdMO-E7TrdZ0zyty1j0ruiDNn2dWZ6Xw_07GLAN3zpy9eJBYsQQofpiJNnCXe-cq951ILVnITSWCBCLN0ESSOoDMQWw6v0BGRg4lg:1ujeF6:RpmxUFq8_5xT3ZM_HaQWL5H769m5MYFogL7VymuZaA8','2025-08-20 13:31:44.519757'),('bz00gvtyalax78f26030xjmkrqimur62','e30:1ujlvn:EoxJ62C3_ra9_epk8PpcoBoJqv_ge6hHo67No_ixQtc','2025-08-20 21:44:19.226357'),('dzzw3vd9lqsjz3x7bkvqbk20d0m6wuea','.eJxVjEEOwiAQRe_C2pARoVNcuu8ZyAwMUjU0Ke3KeHfbpAvd_vfef6tA61LC2mQOY1JXZbw6_Y5M8Sl1J-lB9T7pONVlHlnvij5o08OU5HU73L-DQq1sde99zilaC2wjWEDXofEOz1mQrQGGDSSJPjIxMJGQYUwsrgPTX1B9vg-kOIg:1ul0KV:JwoVmg7qWOMN4dt7lzgvH43cpwphx60phq7nNWjTkx4','2025-08-24 07:18:55.499180'),('g62b61sr5jk57p8tm73igw35jvskqeqh','.eJxVjDEOgzAMRe-SuYqIDcF07M4ZIsdxCm0FEoGp6t0LEkO7vvf-f5vA2zqEregSxmSuxrXm8gsjy1Onw6QHT_fZyjytyxjtkdjTFtvPSV-3s_07GLgM-9oTV4geUDxqRSACOUGnEhPllrz43JBDiLxzl5nAaVcTxqwN1FyZzxcHIDg3:1ulDjf:DTNQ-LDzEf8NvrVRvyGGd1KJeF-cTdsy-lc2y7tq3Cs','2025-08-24 21:37:47.719058'),('i9lb5gsboj7k4yuxbgfjhydcjyxaakrw','.eJxVjMEOwiAQRP-FsyFQLO169O43kGV3laqBpLQn47-XJj3obWbezHxUwHVJYa0yh4nVRYE6_WYR6SV5B_zE_CiaSl7mKeq9og9a9a2wvK9H9-8gYU1t3TlH2IE3RNAkD2Jdc3YUkWEkFgQD0ZyxZwSL9k7ijWfrBSlGBvXdAO0kOL8:1ujkj6:z4Ei1fXryaGU9axayBeGHb_bG1aVemdoxppVgdVtpDI','2025-08-20 20:27:08.813735'),('ibvqteafxc6tij488hav87sf38f7c4ll','.eJxVjMEOwiAQRP-FsyFQLO169O43kGV3laqBpLQn47-XJj3obWbezHxUwHVJYa0yh4nVRYE6_WYR6SV5B_zE_CiaSl7mKeq9og9a9a2wvK9H9-8gYU1t3TlH2IE3RNAkD2Jdc3YUkWEkFgQD0ZyxZwSL9k7ijWfrBSlGBvXdAO0kOL8:1ujm63:RtrR1_rxrtdPU3e1Q9O0P1H0KAYuH5YS2GEidZ7_9R8','2025-08-20 21:54:55.438821'),('iq0jeu8bycpj8cl5ef60qmz97w88wx14','.eJxVjMEOwiAQRP-FsyFQLO169O43kGV3laqBpLQn47-XJj3obWbezHxUwHVJYa0yh4nVRYE6_WYR6SV5B_zE_CiaSl7mKeq9og9a9a2wvK9H9-8gYU1t3TlH2IE3RNAkD2Jdc3YUkWEkFgQD0ZyxZwSL9k7ijWfrBSlGBvXdAO0kOL8:1ujmH3:lMVz0QAx5_Q00NctijtRa8JEXtU5T1CjcO-NCKeqq-E','2025-08-20 22:06:17.211139'),('iza6p7quevn9utwok02za3pl1omcfgk1','.eJxVjDEOgzAMRe-SuYqIDcF07M4ZIsdxCm0FEoGp6t0LEkO7vvf-f5vA2zqEregSxmSuxrXm8gsjy1Onw6QHT_fZyjytyxjtkdjTFtvPSV-3s_07GLgM-9oTV4geUDxqRSACOUGnEhPllrz43JBDiLxzl5nAaVcTxqwN1FyZzxcHIDg3:1ukqow:H3vZ0u92r1pFaRewq6wNRSgy0OwlHRV0rnvLrMmaiHg','2025-08-23 21:09:42.043137'),('ko60f9x9a86ud5f9cfgtcyxl3lz3awo3','.eJxVjEEOwiAQRe_C2hCGFhhduvcMhGEGqZo2Ke3KeHfbpAvd_vfef6uY1qXGtckcB1YXBUGdfkdK-SnjTviRxvuk8zQu80B6V_RBm75NLK_r4f4d1NTqVltGAsoWmYWDQXEgoYQevTHO9YDBA1mwgIAiJVPZaIfdmQmQvVGfLwQ_N7c:1ukV9Q:inVS4IAbevYmc-LYM3HgSUmme7eJrtT67ZCfyP29Fc4','2025-08-22 22:01:24.080857'),('l3v5mknvwmor5s4e0dzj1iguufmk11o3','.eJxVjEEOwiAQRe_C2hAYGAou3XsGAsNUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xKuIswIvT75gTPbjtpNxTu82S5rYuU5a7Ig_a5XUu_Lwc7t9BTb1-azS-ABbMOttB5aBIj4AIgE4Zz4mBrAojOK2Ly84SAQQwrE0AVgOJ9wflPzcD:1ukR5j:P329eP1oT4llHvGh4L7hmcckR_zg8PWuMQaKkW3enOE','2025-08-22 17:41:19.566492'),('liq33yo366rthus7ddr25xyk7butjtua','.eJxVjMsOwiAQAP-FsyF1eXv07jeQZdlK1UBS2pPx3w1JD3qdmcxbRNy3EvfOa1yyuAglTr8sIT25DpEfWO9NUqvbuiQ5EnnYLm8t8-t6tH-Dgr2MrTfgk9EuoA0TaeOTRTzPE7EFh-y1wwTZqICsHBCTI_Q54EzaArD4fAHYjTg9:1uiacB:UPvHxU5HML6kJcQgc2emOd03dXNXBymRLavTNx2xes8','2025-08-17 15:27:11.308715'),('o7lunbzbg1nwvf9n7oefwt0vgbdbfvuc','.eJxVjMEOwiAQRP-FsyFQLO169O43kGV3laqBpLQn47-XJj3obWbezHxUwHVJYa0yh4nVRYE6_WYR6SV5B_zE_CiaSl7mKeq9og9a9a2wvK9H9-8gYU1t3TlH2IE3RNAkD2Jdc3YUkWEkFgQD0ZyxZwSL9k7ijWfrBSlGBvXdAO0kOL8:1ujkgx:K_DZv8UyjpdRX42hVSYfZEZmWFf_T9oIwZXt6h2JbcY','2025-08-20 20:24:55.220679'),('pbxdwac4udul0or4kavcpcwhoh9dapto','.eJxVjDEOgzAMRe-SuYqIDcF07M4ZIsdxCm0FEoGp6t0LEkO7vvf-f5vA2zqEregSxmSuxrXm8gsjy1Onw6QHT_fZyjytyxjtkdjTFtvPSV-3s_07GLgM-9oTV4geUDxqRSACOUGnEhPllrz43JBDiLxzl5nAaVcTxqwN1FyZzxcHIDg3:1ulDld:qcqpYrpvMkrrzuGxaAdoEELphXP1yjQxHplkwTtD9SQ','2025-08-24 21:39:49.438166'),('q6wwc7y9vttsm5rlhgrbldriyu30v4qy','.eJxVjMsOwiAQRf-FtSF0eLt07zeQgQGpGkhKuzL-uzbpQrf3nHNfLOC21rCNvISZ2JmBZqffMWJ65LYTumO7dZ56W5c58l3hBx382ik_L4f7d1Bx1G8dk8reCJti8t6hsVZKPZUJyYIplFEbT84IqdEVj2CTkkoAAOWoHDj2_gALBTe6:1ulOAP:_8s8vkwzbQH4iaUMDnZTDwIGYKI0pocsAXkLnirD0KU','2025-08-25 08:46:05.498600'),('tg0tpi6re04lngddjmp6grkd2bgg6by1','.eJxVjM0OwiAQhN-FsyGUHykevfsMZJddpGogKe3J-O62SQ96mmS-b-YtIqxLiWvnOU4kLsJocfotEdKT607oAfXeZGp1mSeUuyIP2uWtEb-uh_t3UKCXbY0jOGcU6eA4eRdQgwd0WRlvglWBAiaLeiAEHnTGjJYZtNniTBBG8fkCE2c47A:1um6Hi:hSq69mtK1wGAg5QBiYjtJCeAe-vSMu9JjHtGWZHrXSg','2025-08-27 07:52:34.267457'),('u25z1zh2td11ryaesrqsizh08h4p4w83','e30:1ujQXB:UpcQOIV8NMfu0NJ-mh0_OFFrojz0WFZ7oEY4cWBCCrU','2025-08-19 22:53:29.401791'),('vg3bvtijktz1dm31idt6qh305ln3pky0','.eJxVjDsOwjAQBe_iGln-bYgp6XMGa9de4wCypTipEHeHSCmgfTPzXiLgtpawdV7CnMRFaHH63Qjjg-sO0h3rrcnY6rrMJHdFHrTLqSV-Xg_376BgL9_a2MRRu8FhPvtIbCyQcjwq9Bq9AQDyCpzJQIDRZTuiygMiWm2JshLvD-L1OBM:1ujFBl:nnVXyKUHE3kip69XdZybulrqSnkhJp2oO56i6JZ0Xew','2025-08-19 10:46:37.059838'),('wnarliq9ft2sx2sd6sik0s4xopk516mf','.eJxVjDEOgzAMRe-SuYqIDcF07M4ZIsdxCm0FEoGp6t0LEkO7vvf-f5vA2zqEregSxmSuxrXm8gsjy1Onw6QHT_fZyjytyxjtkdjTFtvPSV-3s_07GLgM-9oTV4geUDxqRSACOUGnEhPllrz43JBDiLxzl5nAaVcTxqwN1FyZzxcHIDg3:1ulxnb:id06dNVOv3WEcpSxKvzVwlQ30u6oen8lJjrhwoB-59Q','2025-08-26 22:48:55.585859'),('x2rjjwnjwksf3g7z22qfsp9jxey194da','.eJxVjMsOwiAQAP-FsyF1eXv07jeQZdlK1UBS2pPx3w1JD3qdmcxbRNy3EvfOa1yyuAglTr8sIT25DpEfWO9NUqvbuiQ5EnnYLm8t8-t6tH-Dgr2MrTfgk9EuoA0TaeOTRTzPE7EFh-y1wwTZqICsHBCTI_Q54EzaArD4fAHYjTg9:1uiH9G:HsZg98U-_j4DQ55i6jzoxMI8hlvqKpP5xs0Lu9JIqdM','2025-08-16 18:40:02.335732'),('y4x0oc0orjkp9hr3vj74bb52v97retzb','.eJxVjDsOwjAQBe_iGln-bYgp6XMGa9de4wCypTipEHeHSCmgfTPzXiLgtpawdV7CnMRFaHH63Qjjg-sO0h3rrcnY6rrMJHdFHrTLqSV-Xg_376BgL9_a2MRRu8FhPvtIbCyQcjwq9Bq9AQDyCpzJQIDRZTuiygMiWm2JshLvD-L1OBM:1uiHRa:1juO_YCAggaPgttqHW_ew2147MhuaU2lCgdKANLUw5o','2025-08-16 18:58:58.625471'),('z6wkumusozk7u656b7wbyyj4a50c7szg','.eJxVjMsOwiAQRf-FtSF0eLt07zeQgQGpGkhKuzL-uzbpQrf3nHNfLOC21rCNvISZ2JmBZqffMWJ65LYTumO7dZ56W5c58l3hBx382ik_L4f7d1Bx1G8dk8reCJti8t6hsVZKPZUJyYIplFEbT84IqdEVj2CTkkoAAOWoHDj2_gALBTe6:1ulaZG:1dvDR7dZPLZVUPnG39akmKdTzMcaj3rl0jQDtEz2I3s','2025-08-25 22:00:34.747157');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emails_emaildraft`
--

DROP TABLE IF EXISTS `emails_emaildraft`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails_emaildraft` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recipient` varchar(500) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `emails_emaildraft_created_by_id_f9f24a21_fk_accounts_` (`created_by_id`),
  CONSTRAINT `emails_emaildraft_created_by_id_f9f24a21_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_emaildraft`
--

LOCK TABLES `emails_emaildraft` WRITE;
/*!40000 ALTER TABLE `emails_emaildraft` DISABLE KEYS */;
INSERT INTO `emails_emaildraft` VALUES (1,'infogloex@proton.me','Congratulations','Congratulations','2025-08-09 18:31:17.328984','2025-08-09 21:10:00.496699',17);
/*!40000 ALTER TABLE `emails_emaildraft` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emails_incomingattachment`
--

DROP TABLE IF EXISTS `emails_incomingattachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails_incomingattachment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `content_type` varchar(100) NOT NULL,
  `email_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `emails_incomingattac_email_id_72213482_fk_emails_in` (`email_id`),
  CONSTRAINT `emails_incomingattac_email_id_72213482_fk_emails_in` FOREIGN KEY (`email_id`) REFERENCES `emails_incomingemail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_incomingattachment`
--

LOCK TABLES `emails_incomingattachment` WRITE;
/*!40000 ALTER TABLE `emails_incomingattachment` DISABLE KEYS */;
/*!40000 ALTER TABLE `emails_incomingattachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emails_incomingemail`
--

DROP TABLE IF EXISTS `emails_incomingemail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails_incomingemail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) NOT NULL,
  `sender` varchar(255) NOT NULL,
  `recipient` varchar(255) NOT NULL,
  `body_plain` longtext NOT NULL,
  `body_html` longtext NOT NULL,
  `received_at` datetime(6) NOT NULL,
  `raw_payload` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_incomingemail`
--

LOCK TABLES `emails_incomingemail` WRITE;
/*!40000 ALTER TABLE `emails_incomingemail` DISABLE KEYS */;
/*!40000 ALTER TABLE `emails_incomingemail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emergencies_campaignimage`
--

DROP TABLE IF EXISTS `emergencies_campaignimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergencies_campaignimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(255) NOT NULL,
  `caption` varchar(255) NOT NULL,
  `campaign_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `emergencies_campaign_campaign_id_855a7b77_fk_emergenci` (`campaign_id`),
  CONSTRAINT `emergencies_campaign_campaign_id_855a7b77_fk_emergenci` FOREIGN KEY (`campaign_id`) REFERENCES `emergencies_emergencycampaign` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergencies_campaignimage`
--

LOCK TABLES `emergencies_campaignimage` WRITE;
/*!40000 ALTER TABLE `emergencies_campaignimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `emergencies_campaignimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emergencies_emergencycampaign`
--

DROP TABLE IF EXISTS `emergencies_emergencycampaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergencies_emergencycampaign` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `goal_amount` decimal(12,2) NOT NULL,
  `current_amount` decimal(12,2) NOT NULL,
  `main_image` varchar(255) DEFAULT NULL,
  `video_url` varchar(200) DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `recipient_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `emergencies_emergenc_creator_id_cdc3b4ce_fk_accounts_` (`creator_id`),
  KEY `emergencies_emergenc_recipient_id_852af64e_fk_accounts_` (`recipient_id`),
  CONSTRAINT `emergencies_emergenc_creator_id_cdc3b4ce_fk_accounts_` FOREIGN KEY (`creator_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `emergencies_emergenc_recipient_id_852af64e_fk_accounts_` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergencies_emergencycampaign`
--

LOCK TABLES `emergencies_emergencycampaign` WRITE;
/*!40000 ALTER TABLE `emergencies_emergencycampaign` DISABLE KEYS */;
INSERT INTO `emergencies_emergencycampaign` VALUES (14,'General Donation','We welcome your support at any time. To make a contribution, please visit our secure donation page: https://gloex.org/wallet/donate/. Your generosity will help fund medical aid, emergency relief, famine assistance, educational programs, community development projects, disaster recovery efforts, and other humanitarian initiatives that bring hope and positive change to those in need.',100000.00,1200.00,'image/upload/v1754833129/uqq2lpd8xh1asdt1rwrr.png','https://gloex.org/wallet/donate/','2025-08-09 14:34:05.859311','2026-03-09 16:32:00.000000',1,'active','general-donation',29,29);
/*!40000 ALTER TABLE `emergencies_emergencycampaign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_chatmessage`
--

DROP TABLE IF EXISTS `messaging_chatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_chatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `sender_id` bigint NOT NULL,
  `thread_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `messaging_chatmessag_sender_id_9dffc4f6_fk_accounts_` (`sender_id`),
  KEY `messaging_chatmessage_thread_id_294031b9_fk_messaging_thread_id` (`thread_id`),
  CONSTRAINT `messaging_chatmessag_sender_id_9dffc4f6_fk_accounts_` FOREIGN KEY (`sender_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `messaging_chatmessage_thread_id_294031b9_fk_messaging_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `messaging_thread` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_chatmessage`
--

LOCK TABLES `messaging_chatmessage` WRITE;
/*!40000 ALTER TABLE `messaging_chatmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_chatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_chatpermission`
--

DROP TABLE IF EXISTS `messaging_chatpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_chatpermission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `can_chat` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `recipient_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `messaging_chatpermission_user_id_recipient_id_516b1898_uniq` (`user_id`,`recipient_id`),
  KEY `messaging_chatpermis_recipient_id_26361a9e_fk_accounts_` (`recipient_id`),
  CONSTRAINT `messaging_chatpermis_recipient_id_26361a9e_fk_accounts_` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `messaging_chatpermis_user_id_76f75646_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_chatpermission`
--

LOCK TABLES `messaging_chatpermission` WRITE;
/*!40000 ALTER TABLE `messaging_chatpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_chatpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_message`
--

DROP TABLE IF EXISTS `messaging_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_message`
--

LOCK TABLES `messaging_message` WRITE;
/*!40000 ALTER TABLE `messaging_message` DISABLE KEYS */;
INSERT INTO `messaging_message` VALUES (1,'Hello kibwa','2025-08-02 18:55:22.383855',1,0),(2,'Hello https://www.gloex.org/admin/profiles/userprofile/add/, https://www.gloex.org/admin/profiles/userprofile/add/, https://www.gloex.org/admin/profiles/userprofile/add/, https://www.gloex.org/admin/profiles/userprofile/add/, https://www.gloex.org/admin/profiles/userprofile/add/','2025-08-02 20:09:55.799337',0,0);
/*!40000 ALTER TABLE `messaging_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_thread`
--

DROP TABLE IF EXISTS `messaging_thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_thread` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `updated` datetime(6) NOT NULL,
  `created` datetime(6) NOT NULL,
  `participant1_id` bigint NOT NULL,
  `participant2_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `messaging_thread_participant1_id_participant2_id_eaac56e4_uniq` (`participant1_id`,`participant2_id`),
  KEY `messaging_thread_participant2_id_5e083fdc_fk_accounts_` (`participant2_id`),
  CONSTRAINT `messaging_thread_participant1_id_92c20df8_fk_accounts_` FOREIGN KEY (`participant1_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `messaging_thread_participant2_id_5e083fdc_fk_accounts_` FOREIGN KEY (`participant2_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_thread`
--

LOCK TABLES `messaging_thread` WRITE;
/*!40000 ALTER TABLE `messaging_thread` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_profile`
--

DROP TABLE IF EXISTS `profiles_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bio` longtext NOT NULL,
  `user_id` bigint NOT NULL,
  `category` varchar(100) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `profile_video` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `profiles_profile_user_id_a3e81f91_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_profile`
--

LOCK TABLES `profiles_profile` WRITE;
/*!40000 ALTER TABLE `profiles_profile` DISABLE KEYS */;
INSERT INTO `profiles_profile` VALUES (31,'Welcome to Gloex.org\r\nWe’re excited to have you join our trusted public platform for talented individuals. To begin, please visit the Login or Register page, sign in to your account, and activate your public profile. This will help you connect with new audiences, increase your visibility, and open the door to sponsorship opportunities.\r\n\r\nWe welcome your support at any time. To make a contribution, please visit our secure donation page: https://gloex.org/wallet/donate/. Your generosity will help fund medical aid, emergency relief, famine assistance, educational programs, community development projects, disaster recovery efforts, and other humanitarian initiatives that bring hope and positive change to those in need.\r\n\r\nYour journey to discovery starts here—let the world see your talent.',29,'Administration',1,'image/upload/v1754833183/profile_pictures/tv55tgemfp0qbricuirc.png',NULL),(32,'',30,'General',1,'image/upload/v1754843684/profile_pictures/im2nvb3teze7o4uc6or4.webp',NULL),(33,'',17,'General',1,NULL,NULL),(34,'Weeeeeaaaahjhg',25,'Volleyballer (Pakistan)',1,'image/upload/v1754952035/profile_pictures/ropvqj3ivkiccfaprcaq.png',NULL),(35,'',31,'Footballer (Tanzania)',1,NULL,NULL),(36,'',32,'Artist (Ethiopia)',1,'image/upload/v1755039209/profile_pictures/zxhvmptn6rliwfgr2qbx.jpg',NULL);
/*!40000 ALTER TABLE `profiles_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_profilegallery`
--

DROP TABLE IF EXISTS `profiles_profilegallery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_profilegallery` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(255) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_profilegall_profile_id_afcf26a1_fk_profiles_` (`profile_id`),
  CONSTRAINT `profiles_profilegall_profile_id_afcf26a1_fk_profiles_` FOREIGN KEY (`profile_id`) REFERENCES `profiles_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_profilegallery`
--

LOCK TABLES `profiles_profilegallery` WRITE;
/*!40000 ALTER TABLE `profiles_profilegallery` DISABLE KEYS */;
INSERT INTO `profiles_profilegallery` VALUES (29,'image/upload/v1754813623/profile_gallery/wevww0m42nxu3ld3xxh2.png',1,'2025-08-10 08:13:44.232417',31);
/*!40000 ALTER TABLE `profiles_profilegallery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_sponsorshiprequest`
--

DROP TABLE IF EXISTS `profiles_sponsorshiprequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_sponsorshiprequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `requester_name` varchar(255) NOT NULL,
  `requester_email` varchar(254) NOT NULL,
  `purpose` longtext NOT NULL,
  `action` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_sponsorship_profile_id_b3257be0_fk_profiles_` (`profile_id`),
  CONSTRAINT `profiles_sponsorship_profile_id_b3257be0_fk_profiles_` FOREIGN KEY (`profile_id`) REFERENCES `profiles_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_sponsorshiprequest`
--

LOCK TABLES `profiles_sponsorshiprequest` WRITE;
/*!40000 ALTER TABLE `profiles_sponsorshiprequest` DISABLE KEYS */;
INSERT INTO `profiles_sponsorshiprequest` VALUES (7,'amanda','amanda@gmail.com','i need to support you hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh','connect','2025-08-12 10:23:51.516849',0,34);
/*!40000 ALTER TABLE `profiles_sponsorshiprequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `updates_category`
--

DROP TABLE IF EXISTS `updates_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `updates_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `updates_category`
--

LOCK TABLES `updates_category` WRITE;
/*!40000 ALTER TABLE `updates_category` DISABLE KEYS */;
INSERT INTO `updates_category` VALUES (1,'Announcements','announcements'),(2,'Updates','updates'),(3,'Events','events'),(4,'Opportunities','opportunities'),(5,'competitions','competitions'),(6,'projects','projects');
/*!40000 ALTER TABLE `updates_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `updates_post`
--

DROP TABLE IF EXISTS `updates_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `updates_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `subtitle` varchar(250) DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `body` longtext NOT NULL,
  `featured_image` varchar(255) DEFAULT NULL,
  `featured_video` varchar(255) DEFAULT NULL,
  `attachment` varchar(100) DEFAULT NULL,
  `title_color` varchar(7) NOT NULL,
  `font_size` int unsigned NOT NULL,
  `underline_title` tinyint(1) NOT NULL,
  `status` varchar(2) NOT NULL,
  `published_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `updates_post_author_id_ff20d5d5_fk_accounts_customuser_id` (`author_id`),
  KEY `updates_post_category_id_2b582427_fk_updates_category_id` (`category_id`),
  KEY `updates_post_slug_b3a5ea3d` (`slug`),
  KEY `updates_pos_publish_115855_idx` (`published_at` DESC),
  CONSTRAINT `updates_post_author_id_ff20d5d5_fk_accounts_customuser_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `updates_post_category_id_2b582427_fk_updates_category_id` FOREIGN KEY (`category_id`) REFERENCES `updates_category` (`id`),
  CONSTRAINT `updates_post_chk_1` CHECK ((`font_size` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `updates_post`
--

LOCK TABLES `updates_post` WRITE;
/*!40000 ALTER TABLE `updates_post` DISABLE KEYS */;
INSERT INTO `updates_post` VALUES (8,'THIS IS YOUR TIME',NULL,'this-is-your-time','<p><span style=\"font-size:24px\"><strong>Gloex.org - Official Launch and Guide</strong></span><!-- Use Inter font for a professional look --><!-- Tailwind CSS CDN for easy styling --><!-- Header Section --></p>\r\n\r\n<div class=\"container flex flex-col items-center justify-between mx-auto px-4 sm:flex-row\">&nbsp;\r\n<p><span style=\"font-size:24px\"><strong><a class=\"text-green-700 hover:text-green-900 font-semibold transition-colors duration-200\" href=\"https://gloex.org/\">Home</a> <a class=\"text-green-700 hover:text-green-900 font-semibold transition-colors duration-200\" href=\"https://gloex.org/profiles/discover/\">Discover Talents</a> <a class=\"text-green-700 hover:text-green-900 font-semibold transition-colors duration-200\" href=\"https://gloex.org/sponsor-donate/\">Sponsor &amp; Donate</a>&nbsp;</strong></span><span style=\"font-size:24px\"><strong><a class=\"text-green-700 hover:text-green-900 font-semibold transition-colors duration-200\" href=\"https://gloex.org/emergencies/\">Emergency Aid</a>&nbsp;<a class=\"bg-green-600 text-white px-4 py-2 rounded-full hover:bg-green-700 transition-colors duration-200 shadow-md\" href=\"https://gloex.org/accounts/login/\">Login / Register</a></strong></span></p>\r\n</div>\r\n<!-- Main Content Section --><!-- Welcome Banner Section -->\r\n\r\n<div class=\"#00FF00\">\r\n<div>\r\n<h1><span style=\"color:#000000\"><strong><span style=\"font-size:24px\">Welcome to Gloex.org: Connecting Talent, Support, and Opportunity</span></strong></span></h1>\r\n</div>\r\n</div>\r\n\r\n<div>\r\n<p><span style=\"color:#000000\"><strong><span style=\"font-size:24px\">We are thrilled to announce the official launch of a revolutionary new platform designed to bridge the gap between talented individuals and the opportunities they deserve.</span></strong></span></p>\r\n</div>\r\n\r\n<div class=\"section-separator\">&nbsp;</div>\r\n<!-- How It Works Section -->\r\n\r\n<h2><span style=\"font-size:24px\"><strong>Your Guide to Getting Started</strong></span></h2>\r\n\r\n<div class=\"gap-8 grid lg:grid-cols-3 md:grid-cols-2\"><!-- For Talents Card -->\r\n<div class=\"bg-green-50 border border-green-200 duration-300 hover:scale-105 p-6 rounded-xl shadow-lg transition-transform\">\r\n<h3><span style=\"font-size:24px\"><strong>For Talents</strong></span></h3>\r\n\r\n<p><span style=\"font-size:24px\"><strong>Showcase your skills and creative work. Get discovered by agents, sponsors, and employers. Manage your public profile and track your journey on the platform.</strong></span></p>\r\n<span style=\"font-size:22px\"><strong><a class=\"inline-block bg-green-600 text-white font-semibold py-2 px-6 rounded-full hover:bg-green-700 transition-colors duration-200 shadow-md\" href=\"https://gloex.org/become-talent/\">Become a Talent </a></strong></span></div>\r\n<!-- For Agents Card -->\r\n\r\n<div class=\"bg-green-50 border border-green-200 duration-300 hover:scale-105 p-6 rounded-xl shadow-lg transition-transform\">\r\n<h3><span style=\"font-size:22px\"><strong>For Agents</strong></span></h3>\r\n\r\n<p><span style=\"font-size:22px\"><strong>Act as a professional liaison, scouting and registering talents for commission. Pay a collateral fee to be a verified agent and grow your network.</strong></span></p>\r\n<span style=\"font-size:22px\"><strong><a class=\"inline-block bg-green-600 text-white font-semibold py-2 px-6 rounded-full hover:bg-green-700 transition-colors duration-200 shadow-md\" href=\"https://gloex.org/become-agent/\">Become an Agent </a></strong></span></div>\r\n<!-- For Sponsors & Employers Card -->\r\n\r\n<div class=\"bg-green-50 border border-green-200 duration-300 hover:scale-105 p-6 rounded-xl shadow-lg transition-transform\">\r\n<h3><span style=\"font-size:22px\"><strong>For Sponsors &amp; Employers</strong></span></h3>\r\n\r\n<p><span style=\"font-size:22px\"><strong>Discover talents, support emergency cases, and hire individuals for your team. Find the right people to help you achieve your goals.</strong></span></p>\r\n<span style=\"font-size:22px\"><strong><a class=\"inline-block bg-green-600 text-white font-semibold py-2 px-6 rounded-full hover:bg-green-700 transition-colors duration-200 shadow-md\" href=\"https://gloex.org/sponsor-donate/\">Sponsor &amp; Hire </a></strong></span></div>\r\n</div>\r\n\r\n<div class=\"section-separator\">&nbsp;</div>\r\n<!-- Registration Guide Section -->\r\n\r\n<h2><span style=\"font-size:22px\"><strong>Registration Process</strong></span></h2>\r\n\r\n<div class=\"max-w-2xl mx-auto text-center text-gray-700\">\r\n<p><span style=\"font-size:22px\"><strong>Ready to join the Gloex.org community? The process is simple and secure.</strong></span></p>\r\n\r\n<div class=\"bg-gray-100 border border-gray-200 p-6 rounded-xl\">\r\n<p><span style=\"font-size:22px\"><strong>Registration requires two key steps:</strong></span></p>\r\n\r\n<ul>\r\n	<li><span style=\"font-size:22px\"><strong>✓</strong></span>\r\n\r\n	<div><span style=\"font-size:22px\"><strong>Unique Username: You will be asked to create a unique username that will be your identifier on the platform.</strong></span></div>\r\n	</li>\r\n	<li><span style=\"font-size:22px\"><strong>✓</strong></span>\r\n	<div><span style=\"font-size:22px\"><strong>Strong Password: To ensure your account is secure, your password must be at least 8 characters long and contain a mix of uppercase letters, lowercase letters, numbers, and special characters (e.g., `Password@123`).</strong></span></div>\r\n	</li>\r\n</ul>\r\n</div>\r\n\r\n<div class=\"mt-8\"><span style=\"font-size:22px\"><strong><a class=\"inline-block bg-green-600 text-white font-bold text-lg py-3 px-8 rounded-full hover:bg-green-700 transition-colors duration-200 shadow-lg\" href=\"https://gloex.org/accounts/register/\">Register Now </a></strong></span></div>\r\n</div>\r\n\r\n<div class=\"section-separator\">&nbsp;</div>\r\n<!-- Monetization & Security Section -->\r\n\r\n<h2><span style=\"font-size:22px\"><strong>Fair Monetization &amp; Security</strong></span></h2>\r\n\r\n<div class=\"gap-8 grid items-start max-w-4xl md:grid-cols-2 mx-auto\">\r\n<div class=\"bg-gray-100 border border-gray-200 p-6 rounded-xl\">\r\n<h3><span style=\"font-size:22px\"><strong>Transparent Fees</strong></span></h3>\r\n\r\n<p><span style=\"font-size:22px\"><strong>Gloex.org uses a transparent and fair monetization model to keep the platform running smoothly.</strong></span></p>\r\n\r\n<ul>\r\n	<li><span style=\"font-size:22px\"><strong>Users pay a registration fee.</strong></span></li>\r\n	<li><span style=\"font-size:22px\"><strong>Agents pay a collateral fee.</strong></span></li>\r\n	<li><span style=\"font-size:22px\"><strong>Employers &amp; Clubs pay access fees.</strong></span></li>\r\n</ul>\r\n</div>\r\n\r\n<div class=\"bg-gray-100 border border-gray-200 p-6 rounded-xl\">\r\n<h3><span style=\"font-size:22px\"><strong>Secure Payments</strong></span></h3>\r\n\r\n<p><span style=\"font-size:22px\"><strong>All fees are managed securely through our integration with **NowPayments** for cryptocurrency transactions. We also offer a P2P option for agents to accept fiat payments.</strong></span></p>\r\n<span style=\"font-size:22px\"><strong><a class=\"inline-block bg-gray-900 text-white font-semibold py-2 px-6 rounded-full hover:bg-gray-700 transition-colors duration-200 shadow-md\" href=\"https://gloex.org/wallet/dashboard/\">Manage Wallet </a></strong></span></div>\r\n</div>\r\n<!-- Footer Section -->\r\n\r\n<div class=\"container mx-auto px-4 text-center\">\r\n<h3><span style=\"font-size:22px\"><strong>Join the Gloex.org Community Today!</strong></span></h3>\r\n\r\n<p><span style=\"font-size:22px\"><strong>We are excited to build this global community with you. Discover new opportunities, find the support you need, and make a difference.</strong></span></p>\r\n<span style=\"font-size:22px\"><strong><a class=\"inline-block bg-green-500 text-white font-bold text-lg py-3 px-8 rounded-full hover:bg-green-600 transition-colors duration-200 shadow-lg\" href=\"https://gloex.org/accounts/register/\">Start Your Journey</a></strong></span>\r\n\r\n<div class=\"mt-8 text-gray-400 text-sm\"><span style=\"font-size:22px\"><strong><a class=\"hover:underline mt-2 inline-block\" href=\"https://gloex.org/terms/\">Terms and Conditions</a></strong></span></div>\r\n</div>','image/upload/v1754833296/dsaietstokskszs3zrv2.png',NULL,'','#00ff00',32,1,'PB','2025-08-08 19:59:00.000000','2025-08-08 20:00:59.259736','2025-08-10 13:41:36.492438',17,1);
/*!40000 ALTER TABLE `updates_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `updates_postimage`
--

DROP TABLE IF EXISTS `updates_postimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `updates_postimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(255) NOT NULL,
  `caption` varchar(200) NOT NULL,
  `post_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `updates_postimage_post_id_0234b276_fk_updates_post_id` (`post_id`),
  CONSTRAINT `updates_postimage_post_id_0234b276_fk_updates_post_id` FOREIGN KEY (`post_id`) REFERENCES `updates_post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `updates_postimage`
--

LOCK TABLES `updates_postimage` WRITE;
/*!40000 ALTER TABLE `updates_postimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `updates_postimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wallet_transaction`
--

DROP TABLE IF EXISTS `wallet_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallet_transaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transaction_type` varchar(50) NOT NULL,
  `amount` decimal(18,8) NOT NULL,
  `fee` decimal(10,8) NOT NULL,
  `status` varchar(50) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `description` longtext,
  `transaction_id` char(32) NOT NULL,
  `crypto_currency` varchar(10) DEFAULT NULL,
  `crypto_address` varchar(255) DEFAULT NULL,
  `tx_hash` varchar(255) DEFAULT NULL,
  `nowpayments_payment_id` varchar(255) DEFAULT NULL,
  `amount_received_crypto` decimal(18,8) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_details` longtext,
  `user_proof_of_payment` varchar(100) DEFAULT NULL,
  `admin_payment_instructions` longtext,
  `admin_notes` longtext,
  `receiver_wallet_id` bigint DEFAULT NULL,
  `sender_wallet_id` bigint DEFAULT NULL,
  `wallet_id` bigint DEFAULT NULL,
  `sponsor_id` bigint DEFAULT NULL,
  `sponsor_guest_email` varchar(254) DEFAULT NULL,
  `sponsor_guest_name` varchar(150) DEFAULT NULL,
  `campaign_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_id` (`transaction_id`),
  KEY `wallet_transaction_receiver_wallet_id_be6420da_fk_wallet_wa` (`receiver_wallet_id`),
  KEY `wallet_transaction_sender_wallet_id_959f9643_fk_wallet_wallet_id` (`sender_wallet_id`),
  KEY `wallet_transaction_wallet_id_a0ff1b17_fk_wallet_wallet_id` (`wallet_id`),
  KEY `wallet_transaction_sponsor_id_1591b384_fk_accounts_customuser_id` (`sponsor_id`),
  KEY `wallet_transaction_campaign_id_b87938f0_fk_emergenci` (`campaign_id`),
  CONSTRAINT `wallet_transaction_campaign_id_b87938f0_fk_emergenci` FOREIGN KEY (`campaign_id`) REFERENCES `emergencies_emergencycampaign` (`id`),
  CONSTRAINT `wallet_transaction_receiver_wallet_id_be6420da_fk_wallet_wa` FOREIGN KEY (`receiver_wallet_id`) REFERENCES `wallet_wallet` (`id`),
  CONSTRAINT `wallet_transaction_sender_wallet_id_959f9643_fk_wallet_wallet_id` FOREIGN KEY (`sender_wallet_id`) REFERENCES `wallet_wallet` (`id`),
  CONSTRAINT `wallet_transaction_sponsor_id_1591b384_fk_accounts_customuser_id` FOREIGN KEY (`sponsor_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `wallet_transaction_wallet_id_a0ff1b17_fk_wallet_wallet_id` FOREIGN KEY (`wallet_id`) REFERENCES `wallet_wallet` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wallet_transaction`
--

LOCK TABLES `wallet_transaction` WRITE;
/*!40000 ALTER TABLE `wallet_transaction` DISABLE KEYS */;
INSERT INTO `wallet_transaction` VALUES (64,'emergency_donation_crypto',700.00000000,0.00000000,'completed','2025-08-07 17:03:32.840390','eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee','c84121fbab4547af8186349d6a192d31','btc',NULL,NULL,'5361615410',NULL,NULL,'','','','',NULL,NULL,NULL,17,NULL,NULL,NULL),(65,'emergency_donation_crypto',700.00000000,0.00000000,'expired','2025-08-07 17:06:54.913078','eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee','4a6e36d40d9f4d8ab39ef721e311e40a','btc',NULL,NULL,'5576297484',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,17,NULL,NULL,NULL),(66,'emergency_donation_crypto',399.00000000,80.00000000,'completed','2025-08-07 17:45:52.501314','','ebcd4c982ffd43a1adcb7fa80fc717e5','btc',NULL,NULL,'5049150828',NULL,NULL,'','','','',NULL,NULL,24,17,NULL,NULL,NULL),(67,'manual_credit',399.00000000,0.00000000,'completed','2025-08-07 17:52:49.870295','Admin action: ','6d8ec04f0a9e44fc8975bdf26b78738b',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,'Admin super performed a manual action on 2025-08-07 17:52:49.869158+00:00.',NULL,NULL,24,NULL,NULL,NULL,NULL),(68,'emergency_donation_crypto',500.00000000,0.00000000,'completed','2025-08-07 18:09:21.511850','pole sana','2b0b940450c046e697e7edaf6464c7bf','ltc',NULL,NULL,'4512710869',NULL,NULL,'','','','',NULL,NULL,25,17,NULL,NULL,NULL),(69,'deposit_p2p',200.00000000,0.00000000,'completed','2025-08-07 18:14:54.732648','','e24a40c479b14b0a8176ad40e3bf723b',NULL,NULL,NULL,NULL,NULL,'bank_transfer','','proof_of_payments/StudentInterface_Nepv4Z6.jpg','ydydtfhh 585786976768785785','Approved by super on 2025-08-07 18:18:41.080125+00:00.',NULL,NULL,25,NULL,NULL,NULL,NULL),(70,'deposit_crypto',200.00000000,0.00000000,'expired','2025-08-07 18:19:06.946921',NULL,'d78b8d1c6e094898a3eaf41e194c53f2','btc',NULL,NULL,'5847740250',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,25,NULL,NULL,NULL,NULL),(71,'deposit_crypto',200.00000000,0.00000000,'expired','2025-08-07 18:20:04.533947',NULL,'be743928e9564f9c877181e34d2dd73c','btc',NULL,NULL,'4502736471',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,25,NULL,NULL,NULL,NULL),(72,'sponsorship_crypto',300.00000000,0.00000000,'expired','2025-08-07 18:31:33.490289','Crypto sponsorship for aman. ','1d94e6506c3c4633b41862e72e1dd4f3','btc',NULL,NULL,'5501434104',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,25,17,'','',NULL),(73,'emergency_donation_crypto',7000.00000000,0.00000000,'completed','2025-08-07 18:50:34.048662','','f3b15cfd0cd64250833030abac15ca66','btc',NULL,NULL,'4521197981',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,17,NULL,NULL,NULL),(74,'emergency_donation_crypto',60000.00000000,0.00000000,'completed','2025-08-07 18:52:48.239326','','627c43f23ce3428b820efe72f5c6970f','btc',NULL,NULL,'4958717205',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,17,NULL,NULL,NULL),(75,'emergency_donation_crypto',6000.00000000,0.00000000,'completed','2025-08-07 19:06:35.891587','','0028d5d167cc424d8b6f31362aeb577a','btc',NULL,NULL,'5720722639',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,17,NULL,NULL,NULL),(76,'deposit_crypto',200.00000000,0.00000000,'expired','2025-08-07 21:29:43.338608',NULL,'0e980d11b7414e3e9cd9aa74fc5e928c','usdttrc20',NULL,NULL,'4440485093',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,25,NULL,NULL,NULL,NULL),(77,'deposit_p2p',200.00000000,0.00000000,'awaiting_admin_instructions','2025-08-07 21:32:19.296125','I pay with mtn','bb3d97ed023748c89ac7edef1ff2d4d0',NULL,NULL,NULL,NULL,NULL,'mobile_money','MTN','',NULL,NULL,NULL,NULL,25,NULL,NULL,NULL,NULL),(78,'donation',300.00000000,0.00000000,'expired','2025-08-07 21:47:51.105498',NULL,'2f28d851bf7344999eb119473597a87b','btc',NULL,NULL,'4900980308',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(79,'sponsorship_crypto',200.00000000,0.00000000,'pending','2025-08-08 13:27:43.171522','Crypto sponsorship for ihene. ','2e3563aea8ba4b4cb4eadc40f8b7985c','btc',NULL,NULL,'4739183620',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'shs@hdh.cn','',NULL),(80,'sponsorship_deposit',200.00000000,0.00000000,'awaiting_admin_instructions','2025-08-08 13:28:15.854881','Guest sponsorship from shs@hdh.cn. ','e15eea33825f4e4b911c7d07cbbd1e3f',NULL,NULL,NULL,NULL,NULL,'bank_transfer',NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'shs@hdh.cn','',NULL),(81,'emergency_donation_crypto',600.00000000,0.00000000,'completed','2025-08-10 00:44:10.384340','','d1c11409c3da4e4db50de9853735fdf6','usdttrc20',NULL,NULL,'5734789145',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'a@a.org',NULL,14),(82,'emergency_donation_crypto',600.00000000,0.00000000,'completed','2025-08-10 00:44:11.218157','','26ce8a5eb4134ff3b97250cabcd78b69','usdttrc20',NULL,NULL,'5620729402',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'a@a.org',NULL,14),(83,'donation',50.00000000,0.00000000,'pending','2025-08-10 21:36:30.962945',NULL,'c4c1072017c1450cac62047358459e9a','usdttrc20',NULL,NULL,'4681309115',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(84,'donation',50.00000000,0.00000000,'pending','2025-08-10 21:42:07.127838',NULL,'fc2cba3a34eb4776ad8cc888958b5f41','usdttrc20',NULL,NULL,'5211368136',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(85,'sponsorship_crypto',300.00000000,0.00000000,'completed','2025-08-10 23:02:04.457467','Crypto sponsorship for gloex.org. Message: \'Good\'','9848e435107640febeab24398f14fe64','btc',NULL,NULL,'4557191297',NULL,NULL,'','','','',NULL,NULL,30,NULL,'peter@gloex.org','Peter',NULL),(86,'sponsorship_deposit',300.00000000,0.00000000,'completed','2025-08-10 23:04:02.266512','Guest sponsorship from Peter. Message: \'Hshshbsb\'','c40c1c46973145e48defa8192fdf6924',NULL,NULL,NULL,NULL,NULL,'bank_transfer','','','uy578fg','',NULL,NULL,31,NULL,'peter@gloex.com','Peter',NULL),(87,'emergency_donation_crypto',400.00000000,0.00000000,'pending','2025-08-10 23:23:27.799164','','5d3c70f36e3c4a91b6de3e5ec5d00584','sol',NULL,NULL,'5174021674',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'peter@gloex.com','Peter',14),(88,'emergency_donation_crypto',400.00000000,0.00000000,'pending','2025-08-10 23:23:53.652814','','692d6ccc43224dbdbb652859d95818ba','sol',NULL,NULL,'5512823632',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'peter@gloex.com','Peter',14),(89,'sponsorship_crypto',200.00000000,0.00000000,'pending','2025-08-11 00:06:37.115992','Crypto sponsorship for gloex.org. Message: \'Gkgf\'','7242a41370f04f8da0a10f5ac036a2f3','btc',NULL,NULL,'5861936818',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,30,NULL,'people@gmail.com','People',NULL),(90,'deposit_crypto',32.00000000,0.00000000,'pending','2025-08-11 09:10:42.693628',NULL,'e9d83a8ad86242938dc8e215fd8bff78','btc',NULL,NULL,'5843949694',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,25,NULL,NULL,NULL,NULL),(91,'donation',30.00000000,0.00000000,'pending','2025-08-11 13:01:36.835925',NULL,'163fa44c2efb43988023dde8f54f9299','btc',NULL,NULL,'5229856057',NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(92,'deposit_p2p',200.00000000,0.00000000,'awaiting_admin_instructions','2025-08-12 14:37:11.383843','Momo','2af40df300ae4c74b902a6633c9febda',NULL,NULL,NULL,NULL,NULL,'mobile_money','Momo','',NULL,NULL,NULL,NULL,25,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `wallet_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wallet_wallet`
--

DROP TABLE IF EXISTS `wallet_wallet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallet_wallet` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `balance` decimal(18,8) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `wallet_wallet_user_id_8c75caaa_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wallet_wallet`
--

LOCK TABLES `wallet_wallet` WRITE;
/*!40000 ALTER TABLE `wallet_wallet` DISABLE KEYS */;
INSERT INTO `wallet_wallet` VALUES (24,6399.00000000,'2025-08-07 17:47:56.785085','2025-08-07 19:07:30.719801',24),(25,200.00000000,'2025-08-07 18:02:21.591806','2025-08-07 18:18:41.077841',25),(26,0.00000000,'2025-08-07 18:31:52.428326','2025-08-07 18:31:52.428429',17),(27,0.00000000,'2025-08-07 21:43:44.824688','2025-08-07 21:43:44.824783',26),(30,1200.00000000,'2025-08-09 14:38:05.583177','2025-08-10 13:43:43.009003',29),(31,0.00000000,'2025-08-10 16:29:31.121875','2025-08-10 16:29:31.121979',30),(32,0.00000000,'2025-08-12 15:44:09.039195','2025-08-12 15:44:09.039298',31),(33,0.00000000,'2025-08-12 21:22:02.319804','2025-08-12 21:22:02.319906',32);
/*!40000 ALTER TABLE `wallet_wallet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-15  8:44:12
