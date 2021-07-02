-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3308
-- Generation Time: Feb 01, 2019 at 05:29 AM
-- Server version: 5.6.34-log
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stocks`
--

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `location_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`location_id`) VALUES
('Bangalore'),
('Mumbai'),
('Nasik'),
('Pune');

-- --------------------------------------------------------

--
-- Table structure for table `productmovements`
--

CREATE TABLE `productmovements` (
  `movement_id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `from_location` varchar(255) DEFAULT NULL,
  `to_location` varchar(255) DEFAULT NULL,
  `product_id` varchar(255) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `productmovements`
--

INSERT INTO `productmovements` (`movement_id`, `time`, `from_location`, `to_location`, `product_id`, `qty`) VALUES
(40, '2019-02-01 05:09:50', 'Bangalore', '--', 'P1', 100),
(41, '2019-02-01 05:10:13', 'Bangalore', 'Mumbai', 'P1', 100),
(42, '2019-02-01 05:10:48', 'Mumbai', 'Pune', 'P1', 50),
(43, '2019-02-01 05:11:40', 'Bangalore', '--', 'P2', 30);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`) VALUES
('P1'),
('P2'),
('P3'),
('P4');

-- --------------------------------------------------------

--
-- Table structure for table `product_balance`
--

CREATE TABLE `product_balance` (
  `id` int(11) NOT NULL,
  `product_id` varchar(255) DEFAULT NULL,
  `location_id` varchar(255) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product_balance`
--

INSERT INTO `product_balance` (`id`, `product_id`, `location_id`, `qty`) VALUES
(5, 'P1', 'Bangalore', 0),
(6, 'P1', 'Mumbai', 50),
(7, 'P1', 'Pune', 50),
(8, 'P2', 'Bangalore', 30);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--


CREATE TABLE `users` (
  `id` int auto_increment,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(30),
  `password` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  primary key(`id`,`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`,`address`, `register_date`) VALUES
(1, 'Rucha Mahabal', 'ruchamahabal2@gmail.com', 'rucha08', '$5$rounds=535000$jolEaNj.qShAOtFn$F1gw7pWMtw7rwr.CR9SzhBwhDGFhWnb6SZwNmL5bkCC','Delhi', '2019-01-28 13:49:19');

--
-- Indexes for dumped tables
--



--
-- Table structure for table `maid`
--

CREATE TABLE `maid` (
  `id` int auto_increment ,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(30),
  `password` varchar(100) DEFAULT NULL,
  `mob_no` bigint(10) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `skills` varchar(150) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  primary key(`id`,`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `maid` (`id`, `name`, `email`, `username`, `password`,`mob_no`,`address`,`skills`, `register_date`) VALUES
(1, 'Rucha Mahabal', 'ruchamahabal2@gmail.com', 'rucha08', '$5$rounds=535000$jolEaNj.qShAOtFn$F1gw7pWMtw7rwr.CR9SzhBwhDGFhWnb6SZwNmL5bkCC',888888888,'Delhi','Cleaning Utensils',  '2019-01-28 13:49:19');

ALTER TABLE booking
add COLUMN username varchar(30);

CREATE TABLE `booking` (
  `id` int auto_increment primary key,
  `customer_name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `mob_no` bigint(10) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `job_req` varchar(150) DEFAULT NULL,
  `payment` int(10) DEFAULT NULL,
  `total_days` bigint default NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

# drop table `accepted_request`;

CREATE TABLE `accepted_request` (
  `id` int auto_increment primary key,
  `customer_name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `mob_no` varchar(100) DEFAULT NULL,
  `start_date` varchar(150) DEFAULT NULL,
  `end_date` varchar(150) DEFAULT NULL,
  `payment` varchar(150) DEFAULT NULL,
  `maid_username` varchar(150) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Indexes for table `locations`
--

select * from accepted_request;

INSERT INTO `accepted_request` (`id`, `customer_name`, `address`,`mob_no`,`start_date`,`end_date`, `payment` , `maid_username`,`register_date`) VALUES
(1, 'Rucha Mahabal', 'Mumbai' ,'8888888888', '2021/04/21','2021/05/21' ,'1000', 'maid1', '2019-01-28 13:49:19');


ALTER TABLE `locations`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `productmovements`
--
ALTER TABLE `productmovements`
  ADD PRIMARY KEY (`movement_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `product_balance`
--
ALTER TABLE `product_balance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `productmovements`
--
ALTER TABLE `productmovements`
  MODIFY `movement_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;
--
-- AUTO_INCREMENT for table `product_balance`
--
ALTER TABLE `product_balance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `productmovements`
--
ALTER TABLE `productmovements`
  ADD CONSTRAINT `productmovements_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
