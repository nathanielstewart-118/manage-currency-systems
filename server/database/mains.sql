/*
 Navicat Premium Data Transfer

 Source Server         : local_mysql
 Source Server Type    : MySQL
 Source Server Version : 100432 (10.4.32-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : mains

 Target Server Type    : MySQL
 Target Server Version : 100432 (10.4.32-MariaDB)
 File Encoding         : 65001

 Date: 21/04/2025 02:26:36
*/
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for accounts
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `cur_sys_id` int NOT NULL,
  `uid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts
-- ----------------------------
INSERT INTO `accounts` VALUES (1, 1, '00000000', NULL, NULL);
INSERT INTO `accounts` VALUES (2, 2, '00000001', NULL, NULL);
INSERT INTO `accounts` VALUES (3, 3, '00000002', NULL, NULL);
INSERT INTO `accounts` VALUES (4, 1, '00000003', NULL, NULL);
INSERT INTO `accounts` VALUES (5, 2, '00000004', NULL, NULL);
INSERT INTO `accounts` VALUES (6, 3, '00000005', NULL, NULL);
INSERT INTO `accounts` VALUES (7, 1, '00000006', NULL, NULL);
INSERT INTO `accounts` VALUES (8, 2, '00000007', NULL, NULL);
INSERT INTO `accounts` VALUES (9, 3, '00000008', NULL, NULL);

-- ----------------------------
-- Table structure for currencies
-- ----------------------------
DROP TABLE IF EXISTS `currencies`;
CREATE TABLE `currencies`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `url` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `max_sales_amount` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of currencies
-- ----------------------------
INSERT INTO `currencies` VALUES (1, '円', 'fookomini', 'https://www.48v.me/~fookomini/payment', '日本円です', 0);
INSERT INTO `currencies` VALUES (2, '日本円です', 'ooerice', 'https://www.48v.me/~ooerice/payment', '米台帳の利用者向け', 0);
INSERT INTO `currencies` VALUES (3, '円', 'staff', 'https://www.48v.me/~staff/payment', '社員価格です', 0);

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `command` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `received_json` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sent_json` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of logs
-- ----------------------------

-- ----------------------------
-- Table structure for onetime_suns
-- ----------------------------
DROP TABLE IF EXISTS `onetime_suns`;
CREATE TABLE `onetime_suns`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `onetime_sun` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `owner_sun` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `expired_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 83 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of onetime_suns
-- ----------------------------
INSERT INTO `onetime_suns` VALUES (1, '10858200', 't2', '00000000', '2025-04-18 12:53:07', '2025-04-17 12:53:07', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (2, '10727646', 't1', '00000000', '2025-04-18 12:55:26', '2025-04-18 12:55:26', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (3, '10352376', 't1', '00000000', '2025-04-18 13:01:28', '2025-04-18 13:01:28', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (4, '10604462', 't1', '00000000', '2025-04-18 13:01:39', '2025-04-18 13:01:39', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (5, '10515992', 't1', '00000000', '2025-04-18 13:01:39', '2025-04-18 13:01:39', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (6, '10450548', 't1', '00000000', '2025-04-18 13:01:39', '2025-04-18 13:01:39', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (7, '10328626', 't1', '00000000', '2025-04-18 13:02:15', '2025-04-18 13:02:15', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (8, '10806895', 't1', '00000000', '2025-04-18 13:06:02', '2025-04-18 13:06:02', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (9, '10938850', 't1', '00000000', '2025-04-18 13:08:23', '2025-04-18 13:08:23', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (10, '10858598', 't1', '00000000', '2025-04-18 13:08:52', '2025-04-18 13:08:52', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (11, '10744497', 't1', '00000000', '2025-04-18 13:09:09', '2025-04-18 13:09:09', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (12, '10814796', 't1', '00000000', '2025-04-18 13:10:00', '2025-04-18 13:10:00', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (13, '10904240', 't1', '00000000', '2025-04-18 13:14:06', '2025-04-18 13:14:06', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (14, '10528447', 't1', '00000000', '2025-04-18 13:17:35', '2025-04-18 13:17:35', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (15, '10698977', 't1', '00000000', '2025-04-18 13:18:08', '2025-04-18 13:18:08', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (16, '10981414', 't1', '00000000', '2025-04-19 01:37:46', '2025-04-19 01:37:46', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (17, '10993877', 't1', '00000000', '2025-04-19 02:00:02', '2025-04-19 02:00:02', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (18, '10663842', 't2', '00000000', '2025-04-19 02:00:08', '2025-04-19 02:00:08', '2025-04-19 08:23:53');
INSERT INTO `onetime_suns` VALUES (19, '10542360', 't2', '00000000', '2025-04-19 12:30:06', '2025-04-19 12:30:06', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (20, '10181886', 't2', '00000000', '2025-04-19 12:30:06', '2025-04-19 12:30:06', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (21, '10907028', 't2', '00000000', '2025-04-19 12:31:02', '2025-04-19 12:31:02', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (22, '10220817', 't2', '00000000', '2025-04-19 12:31:02', '2025-04-19 12:31:02', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (23, '10564854', 't2', '00000000', '2025-04-19 12:31:03', '2025-04-19 12:31:03', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (24, '10578665', 't2', '00000000', '2025-04-19 12:39:27', '2025-04-19 12:39:27', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (25, '10495351', 't2', '00000000', '2025-04-19 12:39:27', '2025-04-19 12:39:27', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (26, '10849677', 't2', '00000000', '2025-04-19 12:39:28', '2025-04-19 12:39:28', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (27, '10288133', 't2', '00000000', '2025-04-19 12:40:39', '2025-04-19 12:40:39', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (28, '10643031', 't2', '00000000', '2025-04-19 12:41:03', '2025-04-19 12:41:03', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (29, '10380800', 't2', '00000000', '2025-04-19 14:52:47', '2025-04-19 14:52:47', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (30, '10475161', 't2', '00000000', '2025-04-19 14:58:59', '2025-04-19 14:58:59', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (31, '10530028', 't2', '00000000', '2025-04-19 15:00:10', '2025-04-19 15:00:10', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (32, '10643890', 't2', '00000000', '2025-04-19 15:00:46', '2025-04-19 15:00:46', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (33, '10934747', 't2', '00000000', '2025-04-19 15:00:48', '2025-04-19 15:00:48', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (34, '10581970', 't2', '00000000', '2025-04-19 15:01:33', '2025-04-19 15:01:33', '2025-04-20 02:43:40');
INSERT INTO `onetime_suns` VALUES (35, '10561045', 't1', '00000000', '2025-04-20 05:34:02', '2025-04-20 05:34:02', NULL);
INSERT INTO `onetime_suns` VALUES (36, '10689298', 't4', '00000001', '2025-04-20 05:34:09', '2025-04-20 05:34:09', NULL);
INSERT INTO `onetime_suns` VALUES (37, '10450181', 't4', '00000001', '2025-04-20 06:08:56', '2025-04-20 06:08:56', NULL);
INSERT INTO `onetime_suns` VALUES (38, '10654037', 't4', '00000001', '2025-04-20 06:17:41', '2025-04-20 06:17:41', NULL);
INSERT INTO `onetime_suns` VALUES (39, '10457362', 't4', '00000001', '2025-04-20 06:21:28', '2025-04-20 06:21:28', NULL);
INSERT INTO `onetime_suns` VALUES (40, '10902647', 't4', '00000001', '2025-04-20 06:27:50', '2025-04-20 06:27:50', NULL);
INSERT INTO `onetime_suns` VALUES (41, '10457563', 't4', '00000001', '2025-04-20 06:31:51', '2025-04-20 06:31:51', NULL);
INSERT INTO `onetime_suns` VALUES (42, '10389414', 't4', '00000001', '2025-04-20 06:32:57', '2025-04-20 06:32:57', NULL);
INSERT INTO `onetime_suns` VALUES (43, '10711042', 't4', '00000001', '2025-04-20 06:33:43', '2025-04-20 06:33:43', NULL);
INSERT INTO `onetime_suns` VALUES (44, '10644618', 't4', '00000001', '2025-04-20 06:34:42', '2025-04-20 06:34:42', NULL);
INSERT INTO `onetime_suns` VALUES (45, '10182952', 't4', '00000001', '2025-04-20 06:35:00', '2025-04-20 06:35:00', NULL);
INSERT INTO `onetime_suns` VALUES (46, '10998132', 't1', '00000000', '2025-04-20 06:35:24', '2025-04-20 06:35:24', NULL);
INSERT INTO `onetime_suns` VALUES (47, '10850830', 't1', '00000000', '2025-04-20 06:35:29', '2025-04-20 06:35:29', NULL);
INSERT INTO `onetime_suns` VALUES (48, '10611667', 't1', '00000000', '2025-04-20 06:49:52', '2025-04-20 06:49:52', NULL);
INSERT INTO `onetime_suns` VALUES (49, '10645243', 't4', '00000001', '2025-04-20 06:50:00', '2025-04-20 06:50:00', NULL);
INSERT INTO `onetime_suns` VALUES (51, '10351320', 't4', '00000001', '2025-04-20 07:03:34', '2025-04-20 07:03:34', NULL);
INSERT INTO `onetime_suns` VALUES (52, '10114547', 't4', '00000001', '2025-04-20 07:03:41', '2025-04-20 07:03:41', NULL);
INSERT INTO `onetime_suns` VALUES (53, '10423680', 't4', '00000001', '2025-04-20 07:12:03', '2025-04-20 07:12:03', NULL);
INSERT INTO `onetime_suns` VALUES (54, '10190946', 't4', '00000001', '2025-04-20 07:12:22', '2025-04-20 07:12:22', NULL);
INSERT INTO `onetime_suns` VALUES (55, '10256904', 't4', '00000001', '2025-04-20 07:13:30', '2025-04-20 07:13:30', NULL);
INSERT INTO `onetime_suns` VALUES (56, '10455743', 't4', '00000001', '2025-04-20 07:14:01', '2025-04-20 07:14:01', NULL);
INSERT INTO `onetime_suns` VALUES (57, '10706119', 't4', '00000001', '2025-04-20 07:33:27', '2025-04-20 07:33:27', NULL);
INSERT INTO `onetime_suns` VALUES (58, '10963646', 't4', '00000001', '2025-04-20 07:33:36', '2025-04-20 07:33:36', NULL);
INSERT INTO `onetime_suns` VALUES (59, '10879413', 't4', '00000001', '2025-04-20 07:36:20', '2025-04-20 07:36:20', NULL);
INSERT INTO `onetime_suns` VALUES (60, '10148657', 't4', '00000001', '2025-04-20 07:36:24', '2025-04-20 07:36:24', NULL);
INSERT INTO `onetime_suns` VALUES (61, '10596808', 't4', '00000001', '2025-04-20 07:37:23', '2025-04-20 07:37:23', NULL);
INSERT INTO `onetime_suns` VALUES (62, '10294624', 't4', '00000001', '2025-04-20 07:37:27', '2025-04-20 07:37:27', NULL);
INSERT INTO `onetime_suns` VALUES (63, '10704831', 't4', '00000001', '2025-04-20 07:41:50', '2025-04-20 07:41:50', NULL);
INSERT INTO `onetime_suns` VALUES (64, '10446770', 't4', '00000001', '2025-04-20 07:41:55', '2025-04-20 07:41:55', NULL);
INSERT INTO `onetime_suns` VALUES (65, '10717219', 't4', '00000001', '2025-04-20 07:42:40', '2025-04-20 07:42:40', NULL);
INSERT INTO `onetime_suns` VALUES (66, '10400325', 't4', '00000001', '2025-04-20 07:42:44', '2025-04-20 07:42:44', NULL);
INSERT INTO `onetime_suns` VALUES (67, '10457938', 't4', '00000001', '2025-04-20 07:43:15', '2025-04-20 07:43:15', NULL);
INSERT INTO `onetime_suns` VALUES (68, '10251128', 't4', '00000001', '2025-04-20 07:43:19', '2025-04-20 07:43:19', NULL);
INSERT INTO `onetime_suns` VALUES (69, '10737130', 't4', '00000001', '2025-04-20 07:44:02', '2025-04-20 07:44:02', NULL);
INSERT INTO `onetime_suns` VALUES (70, '10627699', 't4', '00000001', '2025-04-20 07:44:04', '2025-04-20 07:44:04', NULL);
INSERT INTO `onetime_suns` VALUES (71, '10288555', 't4', '00000001', '2025-04-20 07:44:47', '2025-04-20 07:44:47', NULL);
INSERT INTO `onetime_suns` VALUES (72, '10656386', 't4', '00000001', '2025-04-20 07:44:53', '2025-04-20 07:44:53', NULL);
INSERT INTO `onetime_suns` VALUES (73, '10844109', 't4', '00000001', '2025-04-20 07:45:27', '2025-04-20 07:45:27', NULL);
INSERT INTO `onetime_suns` VALUES (74, '10677603', 't4', '00000001', '2025-04-20 07:45:31', '2025-04-20 07:45:31', NULL);
INSERT INTO `onetime_suns` VALUES (75, '10626042', 't4', '00000001', '2025-04-20 07:45:46', '2025-04-20 07:45:46', NULL);
INSERT INTO `onetime_suns` VALUES (76, '10149453', 't4', '00000001', '2025-04-20 07:45:49', '2025-04-20 07:45:49', NULL);
INSERT INTO `onetime_suns` VALUES (77, '10659622', 't1', '00000000', '2025-04-20 07:47:11', '2025-04-20 07:47:11', NULL);
INSERT INTO `onetime_suns` VALUES (78, '10969079', 't4', '00000001', '2025-04-20 07:47:18', '2025-04-20 07:47:18', NULL);
INSERT INTO `onetime_suns` VALUES (79, '10726083', 't4', '00000001', '2025-04-20 07:47:45', '2025-04-20 07:47:45', NULL);
INSERT INTO `onetime_suns` VALUES (80, '10134403', 't4', '00000001', '2025-04-20 07:48:20', '2025-04-20 07:48:20', NULL);
INSERT INTO `onetime_suns` VALUES (81, '10605607', 't4', '00000001', '2025-04-20 07:48:24', '2025-04-20 07:48:24', NULL);
INSERT INTO `onetime_suns` VALUES (82, '10625566', 't4', '00000001', '2025-04-20 07:48:34', '2025-04-20 07:48:34', NULL);

-- ----------------------------
-- Table structure for owners
-- ----------------------------
DROP TABLE IF EXISTS `owners`;
CREATE TABLE `owners`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `owner_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `owner_sun` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `accounts` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `terminals` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  FULLTEXT INDEX `terminal_index`(`terminals`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of owners
-- ----------------------------
INSERT INTO `owners` VALUES (1, 'owner1', '00000000', '[\"1\",\"4\",\"7\"]', '[\"t1\",\"t2\"]');
INSERT INTO `owners` VALUES (2, 'owner2', '00000001', '[\"2\",\"5\",\"8\"]', '[\"t3\",\"t4\"]');
INSERT INTO `owners` VALUES (3, 'owner3', '00000002', '[\"3\",\"6\",\"9\", \"13\"]', '[\"t5\",\"t6\", \"t11\"]');

-- ----------------------------
-- Table structure for pickled-que
-- ----------------------------
DROP TABLE IF EXISTS `pickled-que`;
CREATE TABLE `pickled-que`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sun` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `invalidated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pickled-que
-- ----------------------------

-- ----------------------------
-- Table structure for restocks
-- ----------------------------
DROP TABLE IF EXISTS `restocks`;
CREATE TABLE `restocks`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `current_weight` double NOT NULL,
  `currency_id` int NOT NULL,
  `max_sales_amount` double NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of restocks
-- ----------------------------

-- ----------------------------
-- Table structure for suns
-- ----------------------------
DROP TABLE IF EXISTS `suns`;
CREATE TABLE `suns`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `cur_sys_id` int NOT NULL,
  `uid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sun` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gram` float NOT NULL,
  `max_sales_amount` float NOT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `expired_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of suns
-- ----------------------------

-- ----------------------------
-- Table structure for terminals
-- ----------------------------
DROP TABLE IF EXISTS `terminals`;
CREATE TABLE `terminals`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `area` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `product_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `key_string` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `token` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of terminals
-- ----------------------------
INSERT INTO `terminals` VALUES (1, 't1', '', '商品A', '1234', '7b3291a872c822a86045a00b6087fc92c315136c51fd9aab0dc22ac9e966');
INSERT INTO `terminals` VALUES (2, 't2', '', '商品B', '2234', '097d84d1a43b1b5b6a0e3e1eac622f7ad0b2722d5696e020c729c48018e9');
INSERT INTO `terminals` VALUES (3, 't3', '', '商品C', '2309', '1146c815073f79a00511cb9cfeb3f9fd163d99e57d553e666bfa209918c2');
INSERT INTO `terminals` VALUES (4, 't4', '', '商品B', '3902', '59a44cd0d3b545fb19844445fd7361fd4c21ce87eae7da9301153460a1b3');
INSERT INTO `terminals` VALUES (5, 't5', '', '商品B', '9028', 'd816b45eec2953b851401757e368bb5e5f65272bcdbb4f10b07eb5fd8bbe');
INSERT INTO `terminals` VALUES (6, 't6', '', '商品A', '0921', '9fb0e7b4e890cf1db769ab1bfe940ea49b5f01d76b7bba970f8e55d8f3e5');

SET FOREIGN_KEY_CHECKS = 1;
