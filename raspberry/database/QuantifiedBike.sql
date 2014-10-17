-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 16, 2014 at 05:31 PM
-- Server version: 5.5.40-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `QuantifiedBike`
--

-- --------------------------------------------------------

--
-- Table structure for table `Data`
--

CREATE TABLE IF NOT EXISTS `Data` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Trip` int(11) NOT NULL,
  `DataString` text NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `Trip` (`Trip`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=46 ;

-- --------------------------------------------------------

--
-- Table structure for table `Trips`
--

CREATE TABLE IF NOT EXISTS `Trips` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Data`
--
ALTER TABLE `Data`
  ADD CONSTRAINT `Data_ibfk_1` FOREIGN KEY (`Trip`) REFERENCES `Trips` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
