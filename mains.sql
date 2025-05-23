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

 Date: 06/05/2025 04:59:41
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
INSERT INTO `accounts` VALUES (1, 1, '6Ysg3faW', NULL, NULL);
INSERT INTO `accounts` VALUES (2, 2, 'Mwpuc2dh', NULL, NULL);
INSERT INTO `accounts` VALUES (3, 3, 'fS1rowwm', NULL, NULL);
INSERT INTO `accounts` VALUES (4, 1, 'fbbpAeLN', NULL, NULL);
INSERT INTO `accounts` VALUES (5, 2, 'pJgY6Uzt', NULL, NULL);
INSERT INTO `accounts` VALUES (6, 3, '4WXWG1Ev', NULL, NULL);
INSERT INTO `accounts` VALUES (7, 1, '2UD7Spc1', NULL, NULL);
INSERT INTO `accounts` VALUES (8, 2, 'xL5v6U5t', NULL, NULL);
INSERT INTO `accounts` VALUES (9, 3, 'BQFXCWDn', NULL, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of onetime_suns
-- ----------------------------

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
INSERT INTO `owners` VALUES (1, 'owner1', '00000000', '[\"1\",\"2\",\"3\"]', '[\"t1\",\"t2\"]');
INSERT INTO `owners` VALUES (2, 'owner2', '00000001', '[\"4\",\"5\",\"6\"]', '[\"t3\",\"t4\"]');
INSERT INTO `owners` VALUES (3, 'owner3', '00000002', '[\"7\",\"8\",\"9\", \"13\"]', '[\"t5\",\"t6\", \"t11\"]');

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
