CREATE TABLE `zh_wt`
(
    `mid`          int          NOT NULL AUTO_INCREMENT,
    `username`     varchar(255) NOT NULL,
    `dateModified` varchar(255) DEFAULT NULL,
    `content`      text,
    `personalInfo` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`mid`)
);
