-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2024 at 12:18 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL,
  `client_name` varchar(110) NOT NULL,
  `client_email` varchar(110) NOT NULL,
  `company` varchar(110) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`client_id`, `client_name`, `client_email`, `company`) VALUES
(1, 'Peter Parker', 'email@.com', 'Big Retail Inc.'),
(2, 'Peter Parker', 'email@.com', 'Big Retail Inc.'),
(3, 'Walter White', 'email@.com', 'EduTech Solutions'),
(4, 'Sandra Bullock', 'email@.com', 'Trendsetters Inc.'),
(5, 'Daniel Craig', 'email@.com', 'Gearhead Supply Co.'),
(6, 'Olivia Rodriguez', 'email@.com', 'Fine Dine Group'),
(7, 'Mark Robinson', 'email@.com', 'Green Thumb Gardens'),
(8, 'Emily Blunt', 'email@.com', 'Busy Bees Daycare'),
(9, 'David Kim', 'email@.com', 'Acme Pharmaceuticals'),
(10, 'Matthew McConaughey', 'email@.com', 'Knowledge Stream Inc.'),
(11, 'Jennifer Lopez', 'email@.com', 'Software Craft LLC');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `project_id` int(11) NOT NULL,
  `project_name` varchar(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `requirements` varchar(110) NOT NULL,
  `deadline` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`project_id`, `project_name`, `client_id`, `team_id`, `requirements`, `deadline`) VALUES
(1, 'E-commerce ', 1, 1, 'Extensive documentation', '2024-11-11'),
(2, 'E-commerce ', 2, 2, 'Extensive documentation', '2024-09-17'),
(3, 'Mobile App ', 3, 3, 'Gamified learning modules', '2024-11-03'),
(4, 'Social Medi', 4, 4, 'User-friendly interface with analytics', '2024-11-08'),
(5, 'Inventory M', 5, 5, 'Barcode integration and real-time stock tracking', '0000-00-00'),
(6, 'Restaurant ', 6, 6, 'Online booking with table management', '2024-08-06'),
(7, 'Content Man', 7, 7, 'Drag-and-drop interface for easy content updates', '2024-08-20'),
(8, 'Customer Re', 8, 8, 'Secure parent portal and communication tools', '2024-11-03'),
(9, 'Data Analyt', 9, 9, 'Real-time visualization of key performance indicators (KPIs)', '2024-11-11'),
(10, 'E-learning ', 10, 10, 'Interactive course creation and delivery tools', '2024-11-29'),
(11, 'Bug Trackin', 11, 11, 'Prioritization and collaboration features for bug reporting', '2024-07-01');

-- --------------------------------------------------------

--
-- Table structure for table `team_members`
--

CREATE TABLE `team_members` (
  `team_id` int(11) NOT NULL,
  `teamlead` varchar(200) NOT NULL,
  `member1` varchar(200) DEFAULT NULL,
  `member2` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `team_members`
--

INSERT INTO `team_members` (`team_id`, `teamlead`, `member1`, `member2`) VALUES
(1, 'Alice Brown', 'David Lee', ''),
(2, 'Alice Brown', 'Jane Doe', ''),
(3, 'David Lee', 'Michael Young, Emily Chen', 'Emily Chen'),
(4, 'Alice Brown', 'Jane Doe, William Green', 'William Green'),
(5, 'David Lee', 'Michael Young, Emily Chen', ' Emily Chen'),
(6, 'Alice Brown', 'William Green, Sarah Jones', 'Sarah Jones'),
(7, 'David Lee', 'Jane Doe, Michael Young', ' Michael Young'),
(8, 'Alice Brown', 'William Green, Sarah Jones', ' Sarah Jones'),
(9, 'David Lee', 'Michael Young, Emily Chen', ' Emily Chen'),
(10, 'Alice Brown', 'Jane Doe, William Green', 'William Green'),
(11, 'David Lee', 'Michael Young, Sarah Jones', ' Sarah Jones');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`client_id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`project_id`),
  ADD KEY `clientconnect` (`client_id`),
  ADD KEY `teamconnect` (`team_id`);

--
-- Indexes for table `team_members`
--
ALTER TABLE `team_members`
  ADD PRIMARY KEY (`team_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `clientconnect` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `teamconnect` FOREIGN KEY (`team_id`) REFERENCES `team_members` (`team_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
