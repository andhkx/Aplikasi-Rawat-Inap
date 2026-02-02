-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 20, 2026 at 03:34 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_rawatinap_dhika`
--

-- --------------------------------------------------------

--
-- Table structure for table `kamar_dhika`
--

CREATE TABLE `kamar_dhika` (
  `id_kamar` varchar(5) NOT NULL,
  `no_kamar` int(2) NOT NULL,
  `kelas` enum('I','II','III') NOT NULL,
  `status_kamar` enum('Reguler','Vip') NOT NULL,
  `harga` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kamar_dhika`
--

INSERT INTO `kamar_dhika` (`id_kamar`, `no_kamar`, `kelas`, `status_kamar`, `harga`) VALUES
('KM001', 1, 'III', 'Reguler', 200000),
('KM002', 2, 'III', 'Reguler', 200000),
('KM003', 1, 'II', 'Reguler', 300000),
('KM004', 1, 'I', 'Vip', 500000),
('KM005', 2, 'I', 'Vip', 500000);

-- --------------------------------------------------------

--
-- Table structure for table `pasien_dhika`
--

CREATE TABLE `pasien_dhika` (
  `id_pasien` varchar(5) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `alamat` varchar(50) NOT NULL,
  `kontak` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pasien_dhika`
--

INSERT INTO `pasien_dhika` (`id_pasien`, `nama`, `alamat`, `kontak`) VALUES
('PS001', 'Andhika Andriana Putra', 'Jl. Kolmas', '0895627174900'),
('PS002', 'Aditya Firmansyah', 'Jl. Sangkuriang', '081354456987'),
('PS003', 'Ahmad Dani', 'Jl. Unjani', '082665413512'),
('PS004', 'Haidar Alif', 'Jl. Puri', '08456798522'),
('PS005', 'Andika Gustiawan', 'Jl. Pojok', '085566213945');

-- --------------------------------------------------------

--
-- Table structure for table `rawatinap_dhika`
--

CREATE TABLE `rawatinap_dhika` (
  `id_rawat` varchar(6) NOT NULL,
  `id_pasien` varchar(6) NOT NULL,
  `id_kamar` varchar(6) NOT NULL,
  `tgl_masuk` date NOT NULL,
  `tgl_keluar` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rawatinap_dhika`
--

INSERT INTO `rawatinap_dhika` (`id_rawat`, `id_pasien`, `id_kamar`, `tgl_masuk`, `tgl_keluar`) VALUES
('RW001', 'PS001', 'KM001', '2026-01-01', '2026-01-02'),
('RW002', 'PS002', 'KM002', '2026-01-01', '2026-01-03'),
('RW003', 'PS003', 'KM003', '2026-01-01', '2026-01-07'),
('RW004', 'PS004', 'KM004', '2026-01-08', '2026-01-13'),
('RW005', 'PS005', 'KM005', '2026-01-01', '2026-01-19');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_dhika`
--

CREATE TABLE `transaksi_dhika` (
  `id_transaksi` varchar(5) NOT NULL,
  `id_pasien` varchar(5) NOT NULL,
  `total_biaya` int(8) NOT NULL,
  `status_pembayaran` enum('Lunas','Belum Lunas') NOT NULL,
  `tgl` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi_dhika`
--

INSERT INTO `transaksi_dhika` (`id_transaksi`, `id_pasien`, `total_biaya`, `status_pembayaran`, `tgl`) VALUES
('TR001', 'PS001', 200000, 'Lunas', '2026-01-02'),
('TR002', 'PS002', 400000, 'Lunas', '2026-01-04'),
('TR003', 'PS003', 1800000, 'Lunas', '2026-01-07'),
('TR004', 'PS004', 2500000, 'Belum Lunas', '2026-01-13'),
('TR005', 'PS005', 9000000, 'Lunas', '2026-01-20');

-- --------------------------------------------------------

--
-- Table structure for table `user_dhika`
--

CREATE TABLE `user_dhika` (
  `id_user` varchar(10) NOT NULL,
  `role` enum('Admin','User') NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_dhika`
--

INSERT INTO `user_dhika` (`id_user`, `role`, `username`, `password`) VALUES
('US001', 'User', 'dikaaw', 'andhika123'),
('US002', 'User', 'adit', 'adit123'),
('US003', 'User', 'dani', 'dani123'),
('US004', 'User', 'ncep', 'haidar123'),
('US005', 'User', 'iting', 'iting123'),
('US006', 'Admin', 'admin', 'admin123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar_dhika`
--
ALTER TABLE `kamar_dhika`
  ADD PRIMARY KEY (`id_kamar`);

--
-- Indexes for table `pasien_dhika`
--
ALTER TABLE `pasien_dhika`
  ADD PRIMARY KEY (`id_pasien`);

--
-- Indexes for table `rawatinap_dhika`
--
ALTER TABLE `rawatinap_dhika`
  ADD PRIMARY KEY (`id_rawat`),
  ADD KEY `id_pasien` (`id_pasien`) USING BTREE,
  ADD KEY `id_kamar` (`id_kamar`) USING BTREE;

--
-- Indexes for table `transaksi_dhika`
--
ALTER TABLE `transaksi_dhika`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_pasien` (`id_pasien`);

--
-- Indexes for table `user_dhika`
--
ALTER TABLE `user_dhika`
  ADD PRIMARY KEY (`id_user`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rawatinap_dhika`
--
ALTER TABLE `rawatinap_dhika`
  ADD CONSTRAINT `rawatinap_dhika_ibfk_1` FOREIGN KEY (`id_kamar`) REFERENCES `kamar_dhika` (`id_kamar`),
  ADD CONSTRAINT `rawatinap_dhika_ibfk_2` FOREIGN KEY (`id_pasien`) REFERENCES `pasien_dhika` (`id_pasien`);

--
-- Constraints for table `transaksi_dhika`
--
ALTER TABLE `transaksi_dhika`
  ADD CONSTRAINT `transaksi_dhika_ibfk_1` FOREIGN KEY (`id_pasien`) REFERENCES `pasien_dhika` (`id_pasien`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
