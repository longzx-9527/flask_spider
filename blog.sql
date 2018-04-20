/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50721
Source Host           : 192.168.66.188:3306
Source Database       : blog

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-04-20 10:25:08
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for fiction
-- ----------------------------
DROP TABLE IF EXISTS `fiction`;
CREATE TABLE `fiction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fiction_name` varchar(255) NOT NULL,
  `fiction_id` varchar(255) NOT NULL,
  `fiction_real_url` varchar(255) DEFAULT NULL,
  `fiction_img` varchar(255) DEFAULT NULL,
  `fiction_author` char(30) DEFAULT NULL,
  `fiction_comment` varchar(255) DEFAULT NULL,
  `fiction_count` int(11) DEFAULT NULL,
  `update` varchar(255) DEFAULT NULL,
  `new_content` varchar(255) DEFAULT NULL,
  `new_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fiction_id` (`fiction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fiction_content
-- ----------------------------
DROP TABLE IF EXISTS `fiction_content`;
CREATE TABLE `fiction_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fiction_url` varchar(255) NOT NULL,
  `fiction_content` longtext NOT NULL,
  `fiction_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fiction_content_index` (`fiction_url`,`fiction_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3273 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fiction_lst
-- ----------------------------
DROP TABLE IF EXISTS `fiction_lst`;
CREATE TABLE `fiction_lst` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fiction_name` varchar(255) NOT NULL,
  `fiction_id` varchar(255) NOT NULL,
  `fiction_lst_url` varchar(255) NOT NULL,
  `fiction_lst_name` varchar(255) NOT NULL,
  `fiction_real_url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fiction_lst_index` (`fiction_lst_url`,`fiction_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
