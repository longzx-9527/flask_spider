/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50721
Source Host           : 192.168.66.188:3306
Source Database       : blog

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-04-25 08:39:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `article_id` varchar(20) NOT NULL,
  `article_title` varchar(100) NOT NULL,
  `article_text` text,
  `article_summary` varchar(255) DEFAULT NULL,
  `article_read_cnt` int(11) DEFAULT NULL,
  `article_sc` int(11) DEFAULT NULL,
  `article_pl` int(11) DEFAULT NULL,
  `article_date` datetime DEFAULT NULL,
  `article_url` text,
  `article_type` varchar(10) DEFAULT NULL,
  `article_author` varchar(20) DEFAULT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `comment_id` varchar(20) NOT NULL,
  `comment_text` text,
  `comment_date` datetime DEFAULT NULL,
  `user_id` varchar(20) NOT NULL,
  `article_id` varchar(20) NOT NULL,
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for commparam
-- ----------------------------
DROP TABLE IF EXISTS `commparam`;
CREATE TABLE `commparam` (
  `param_name` varchar(10) NOT NULL,
  `param_value` int(11) DEFAULT NULL,
  `param_text` varchar(100) DEFAULT NULL,
  `param_stat` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`param_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fiction
-- ----------------------------
DROP TABLE IF EXISTS `fiction`;
CREATE TABLE `fiction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fiction_name` varchar(255) DEFAULT NULL,
  `fiction_id` varchar(255) DEFAULT NULL,
  `fiction_real_url` varchar(255) DEFAULT NULL,
  `fiction_img` varchar(255) DEFAULT NULL,
  `fiction_author` char(30) DEFAULT NULL,
  `fiction_comment` varchar(255) DEFAULT NULL,
  `update` varchar(255) DEFAULT NULL,
  `new_content` varchar(255) DEFAULT NULL,
  `new_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fiction_content
-- ----------------------------
DROP TABLE IF EXISTS `fiction_content`;
CREATE TABLE `fiction_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fiction_url` varchar(255) DEFAULT NULL,
  `fiction_content` longtext,
  `fiction_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3274 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fiction_lst
-- ----------------------------
DROP TABLE IF EXISTS `fiction_lst`;
CREATE TABLE `fiction_lst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fiction_name` varchar(255) DEFAULT NULL,
  `fiction_id` varchar(255) DEFAULT NULL,
  `fiction_lst_url` varchar(255) DEFAULT NULL,
  `fiction_lst_name` varchar(255) DEFAULT NULL,
  `fiction_real_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7646 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` varchar(20) NOT NULL,
  `user_name` varchar(30) DEFAULT NULL,
  `nickname` varchar(40) DEFAULT NULL,
  `sex` varchar(4) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `last_login_tm` datetime DEFAULT NULL,
  `user_crt_dt` datetime DEFAULT NULL,
  `attention_cnt` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
