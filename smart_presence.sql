-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 27, 2024 at 03:17 AM
-- Server version: 8.0.30
-- PHP Version: 8.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;

--
-- Database: `smart_presence`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
    `id` int NOT NULL,
    `user_id` int NOT NULL,
    `room_id` int NOT NULL,
    `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO
    `attendance` (
        `id`,
        `user_id`,
        `room_id`,
        `timestamp`
    )
VALUES (
        58,
        6,
        1,
        '2024-07-25 17:53:39'
    ),
    (
        59,
        6,
        2,
        '2024-07-26 12:45:13'
    );

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
    `id` int NOT NULL,
    `name` varchar(100) NOT NULL,
    `capacity` int NOT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO
    `rooms` (
        `id`,
        `name`,
        `capacity`,
        `created_at`,
        `updated_at`
    )
VALUES (
        1,
        '3.1',
        30,
        '2024-07-24 17:05:22',
        '2024-07-24 17:05:22'
    ),
    (
        2,
        '3.2',
        30,
        '2024-07-24 17:05:22',
        '2024-07-24 17:05:22'
    ),
    (
        3,
        '3.3',
        30,
        '2024-07-24 17:05:22',
        '2024-07-24 17:05:22'
    ),
    (
        4,
        '3.4',
        30,
        '2024-07-24 17:05:22',
        '2024-07-24 17:05:22'
    ),
    (
        5,
        '3.5',
        30,
        '2024-07-24 17:05:22',
        '2024-07-24 17:05:22'
    );

-- --------------------------------------------------------

--
-- Table structure for table `room_conditions`
--

CREATE TABLE `room_conditions` (
    `id` int NOT NULL,
    `room_id` int NOT NULL,
    `setting_ac_temp` float NOT NULL,
    `temperature` float NOT NULL,
    `recorded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `room_conditions`
--

INSERT INTO
    `room_conditions` (
        `id`,
        `room_id`,
        `setting_ac_temp`,
        `temperature`,
        `recorded_at`
    )
VALUES (
        1,
        1,
        0,
        26,
        '2024-07-24 17:06:36'
    ),
    (
        2,
        1,
        0,
        22,
        '2024-07-24 17:07:25'
    ),
    (
        3,
        1,
        28,
        25,
        '2024-07-24 17:06:36'
    ),
    (
        4,
        1,
        28,
        25,
        '2024-07-24 17:06:36'
    ),
    (
        5,
        1,
        28,
        25,
        '2024-07-25 08:20:15'
    ),
    (
        6,
        1,
        28,
        22.2,
        '2024-07-25 08:33:42'
    ),
    (
        7,
        1,
        28,
        22.2,
        '2024-07-25 08:33:58'
    ),
    (
        8,
        1,
        28,
        22.2,
        '2024-07-25 08:34:14'
    ),
    (
        9,
        1,
        28,
        25.4,
        '2024-07-25 08:54:57'
    ),
    (
        10,
        1,
        28,
        27.6,
        '2024-07-25 08:55:13'
    ),
    (
        11,
        1,
        28,
        27.6,
        '2024-07-25 08:55:38'
    ),
    (
        12,
        1,
        28,
        27.6,
        '2024-07-25 08:55:50'
    ),
    (
        13,
        1,
        28,
        29.3,
        '2024-07-25 12:51:52'
    ),
    (
        14,
        1,
        28,
        28.9,
        '2024-07-25 14:17:41'
    ),
    (
        15,
        1,
        28,
        28.9,
        '2024-07-25 14:17:57'
    ),
    (
        16,
        1,
        28,
        28.9,
        '2024-07-25 14:18:25'
    ),
    (
        17,
        1,
        28,
        28.9,
        '2024-07-25 14:18:35'
    ),
    (
        18,
        1,
        28,
        28.9,
        '2024-07-25 14:18:45'
    ),
    (
        19,
        1,
        28,
        28.9,
        '2024-07-25 14:18:55'
    ),
    (
        20,
        1,
        28,
        28.9,
        '2024-07-25 14:20:12'
    ),
    (
        21,
        1,
        28,
        28.9,
        '2024-07-25 14:20:22'
    ),
    (
        22,
        1,
        28,
        28.9,
        '2024-07-25 14:20:32'
    ),
    (
        23,
        1,
        28,
        28.9,
        '2024-07-25 14:20:43'
    ),
    (
        24,
        1,
        28,
        28.9,
        '2024-07-25 14:21:00'
    ),
    (
        25,
        1,
        28,
        28.9,
        '2024-07-25 14:23:01'
    ),
    (
        26,
        1,
        28,
        28.9,
        '2024-07-25 14:27:50'
    ),
    (
        27,
        1,
        28,
        28.9,
        '2024-07-25 14:28:11'
    ),
    (
        28,
        1,
        28,
        14.4,
        '2024-07-25 14:29:57'
    ),
    (
        29,
        1,
        28,
        28.9,
        '2024-07-25 14:30:59'
    ),
    (
        30,
        1,
        28,
        14.4,
        '2024-07-25 14:32:01'
    ),
    (
        31,
        1,
        28,
        28.9,
        '2024-07-25 14:33:25'
    ),
    (
        32,
        1,
        28,
        28.9,
        '2024-07-25 14:34:26'
    ),
    (
        33,
        1,
        28,
        28.9,
        '2024-07-25 14:35:28'
    ),
    (
        34,
        1,
        28,
        28.9,
        '2024-07-25 14:43:11'
    ),
    (
        35,
        1,
        28,
        28.9,
        '2024-07-25 14:44:12'
    ),
    (
        36,
        1,
        28,
        28.9,
        '2024-07-25 14:48:42'
    );

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
    `id` int NOT NULL,
    `name` varchar(100) NOT NULL,
    `face_id` varchar(255) NOT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO
    `users` (
        `id`,
        `name`,
        `face_id`,
        `created_at`,
        `updated_at`
    )
VALUES (
        4,
        'Dila Adelia Juliarti',
        '81e25956-5574-49d1-a0dc-3fd2e36f0e5e',
        '2024-07-25 01:00:31',
        '2024-07-25 01:00:31'
    ),
    (
        5,
        'Latansa Bima Amanta',
        '9a4a97a7-c5aa-4c4b-8954-2a4481f82850',
        '2024-07-25 01:00:31',
        '2024-07-25 01:00:31'
    ),
    (
        6,
        'Muhammad Rayasya Dziqi Cahyana',
        'bd882328-9236-443f-ab38-e132b8f95657',
        '2024-07-25 01:00:31',
        '2024-07-25 01:00:31'
    );

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
ADD PRIMARY KEY (`id`),
ADD KEY `users_id` (`user_id`) USING BTREE,
ADD KEY `rooms_id` (`room_id`) USING BTREE;

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms` ADD PRIMARY KEY (`id`);

--
-- Indexes for table `room_conditions`
--
ALTER TABLE `room_conditions`
ADD PRIMARY KEY (`id`),
ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `face_id` (`face_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
MODIFY `id` int NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 60;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
MODIFY `id` int NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 6;

--
-- AUTO_INCREMENT for table `room_conditions`
--
ALTER TABLE `room_conditions`
MODIFY `id` int NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 37;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
MODIFY `id` int NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

--
-- Constraints for table `room_conditions`
--
ALTER TABLE `room_conditions`
ADD CONSTRAINT `room_conditions_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;