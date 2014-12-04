-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 04, 2014 at 11:15 AM
-- Server version: 5.5.40-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `QuantifiedBike`
--
CREATE DATABASE IF NOT EXISTS `QuantifiedBike` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `QuantifiedBike`;

-- --------------------------------------------------------

--
-- Table structure for table `Data`
--

DROP TABLE IF EXISTS `Data`;
CREATE TABLE IF NOT EXISTS `Data` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Trip` int(11) NOT NULL,
  `DataString` text NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `Trip` (`Trip`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=585 ;

-- --------------------------------------------------------

--
-- Table structure for table `Images`
--

DROP TABLE IF EXISTS `Images`;
CREATE TABLE IF NOT EXISTS `Images` (
  `Trip` int(11) NOT NULL,
  `ImageName` varchar(100) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `ImageName` (`ImageName`),
  KEY `Trip` (`Trip`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Trips`
--

DROP TABLE IF EXISTS `Trips`;
CREATE TABLE IF NOT EXISTS `Trips` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `StartTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `EndTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Data`
--
ALTER TABLE `Data`
  ADD CONSTRAINT `Data_ibfk_1` FOREIGN KEY (`Trip`) REFERENCES `Trips` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Images`
--
ALTER TABLE `Images`
  ADD CONSTRAINT `Images_ibfk_1` FOREIGN KEY (`Trip`) REFERENCES `Trips` (`Id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
