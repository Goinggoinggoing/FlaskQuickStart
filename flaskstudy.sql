/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : localhost:3306
 Source Schema         : flaskstudy

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : 65001

 Date: 27/02/2025 22:27:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for score
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score`  (
  `score_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `score_value` float NOT NULL,
  `semester` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_deleted` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '0',
  `status_id` int(11) NULL DEFAULT 1,
  `add_date` varchar(23) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `add_user_id` int(11) NULL DEFAULT NULL,
  `edit_date` varchar(23) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `edit_user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`score_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7476105300174438401 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of score
-- ----------------------------
INSERT INTO `score` VALUES (12, 1, '数学', 89.5, '2024 春季', '1', 0, '2024-02-26 10:00:00', 1, NULL, NULL);
INSERT INTO `score` VALUES (13, 2, '英语', 5, '2024 春季', '1', 1, '2024-02-26 10:10:00', 1, '2024-02-26 12:30:00', 1);
INSERT INTO `score` VALUES (14, 3, '物理', 78, '2024 春季', '0', 1, '2024-02-26 10:15:00', 1, NULL, NULL);
INSERT INTO `score` VALUES (15, 4, '化学', 85, '2024 春季', '0', 1, '2024-02-26 10:20:00', 1, NULL, NULL);
INSERT INTO `score` VALUES (16, 5, '数学', 75.5, '2024 秋季', '0', 1, '2024-02-26 10:25:00', 1, NULL, NULL);
INSERT INTO `score` VALUES (17, 6, '英语', 88, '2024 秋季', '0', 1, '2024-02-26 10:30:00', 1, NULL, NULL);
INSERT INTO `score` VALUES (18, 7, '历史', 91.5, '2024 春季', '0', 1, '2024-02-26 10:35:00', 1, NULL, NULL);
INSERT INTO `score` VALUES (19, 8, '地理', 80, '2024 秋季', '0', 1, '2024-02-26 10:40:00', 1, NULL, NULL);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `created_date` datetime(6) NULL DEFAULT NULL,
  `modified_date` datetime(6) NULL DEFAULT NULL,
  `id` bigint(20) UNSIGNED NOT NULL,
  `nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `pw_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `avatar_id` bigint(20) UNSIGNED NULL DEFAULT NULL,
  `is_ban` tinyint(1) NULL DEFAULT NULL,
  `is_admin` tinyint(1) NULL DEFAULT NULL,
  `purpose` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `identity` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `field` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `address` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `postal_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `we_mini_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `nickname`(`nickname`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  UNIQUE INDEX `we_mini_id`(`we_mini_id`) USING BTREE,
  INDEX `ix_user_created_date`(`created_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('2025-02-27 20:40:29.000000', '2025-02-27 20:40:31.000000', 7476030207059558401, 'test', 'test', 'test@example.com', '12345678', 'pbkdf2:sha256:260000$eR1TRr8NeVT0e2n9$6307cecf43670ca05aacc42893a8c14d644aedec35bfd6ea2b3d0a07d809a16d', NULL, 0, 0, '测试用途', '研究员', '计算机科学', '北京市海淀区', '100080', NULL);

SET FOREIGN_KEY_CHECKS = 1;
