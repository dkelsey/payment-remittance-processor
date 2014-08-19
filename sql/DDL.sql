-- MySQL dump 10.13  Distrib 5.6.17, for osx10.9 (x86_64)
--
-- Host: localhost    Database: bvb
-- ------------------------------------------------------
-- Server version	5.6.17-debug-log

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
-- Current Database: `bvb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `bvb` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `bvb`;

--
-- Table structure for table `ldb_batches`
--

DROP TABLE IF EXISTS `ldb_batches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ldb_batches` (
  `batchid` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(64) DEFAULT NULL,
  `process_date` date DEFAULT NULL,
  PRIMARY KEY (`batchid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ldb_batchesdata`
--

DROP TABLE IF EXISTS `ldb_batchesdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ldb_batchesdata` (
  `batchid` int(11) DEFAULT NULL,
  `store_number` int(11) DEFAULT NULL,
  `transaction_type` varchar(32) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `invoice_reference_number` int(11) DEFAULT NULL,
  `original_invoice_number` int(11) DEFAULT NULL,
  `customer_number` int(11) DEFAULT NULL,
  `customer_type` varchar(32) DEFAULT NULL,
  `customer_name` varchar(32) DEFAULT NULL,
  `customer_phone_Number` varchar(32) DEFAULT NULL,
  `customer_address` varchar(32) DEFAULT NULL,
  `customer_city` varchar(32) DEFAULT NULL,
  `customer_province` varchar(32) DEFAULT NULL,
  `customer_postal_code` varchar(7) DEFAULT NULL,
  `payment_method` varchar(32) DEFAULT NULL,
  `SKU` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `display_price` decimal(15,2) DEFAULT NULL,
  `container_deposit` decimal(15,2) DEFAULT NULL,
  `total_doc_amount` decimal(15,2) DEFAULT NULL,
  `return_reason_code` varchar(32) DEFAULT NULL,
  `pipeline_sales` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paymentremittance`
--

DROP TABLE IF EXISTS `paymentremittance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paymentremittance` (
  `paymentremittanceid` int(11) NOT NULL AUTO_INCREMENT,
  `payeename` varchar(64) DEFAULT NULL,
  `payeeid` int(11) DEFAULT NULL,
  `payeesite` varchar(64) DEFAULT NULL,
  `paymentnumber` int(11) DEFAULT NULL,
  `paymentdate` date DEFAULT NULL,
  `filename` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`paymentremittanceid`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paymentremittancedata`
--

DROP TABLE IF EXISTS `paymentremittancedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paymentremittancedata` (
  `paymentremittanceid` bigint(20) DEFAULT NULL,
  `invoiceNumber` varchar(32) DEFAULT NULL,
  `orderType` varchar(32) DEFAULT NULL,
  `orderNumber` varchar(32) DEFAULT NULL,
  `store` int(11) DEFAULT NULL,
  `billOfLading` int(11) DEFAULT NULL,
  `transactionDate` date DEFAULT NULL,
  `batchDate` date DEFAULT NULL,
  `SKU` int(11) DEFAULT NULL,
  `product` varchar(64) DEFAULT NULL,
  `UPC` varchar(32) DEFAULT NULL,
  `size` float DEFAULT NULL,
  `supplierID` int(11) DEFAULT NULL,
  `supplierName` varchar(64) DEFAULT NULL,
  `reason` varchar(64) DEFAULT NULL,
  `reference` varchar(64) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `UOM` varchar(32) DEFAULT NULL,
  `cost` decimal(15,2) DEFAULT NULL,
  `GST` decimal(15,2) DEFAULT NULL,
  `containerDeposit` varchar(64) DEFAULT NULL,
  `freightAllowance` varchar(64) DEFAULT NULL,
  `total` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-18 18:03:42
