BEGIN;
CREATE TABLE `PortVulns` (
    `pvid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `Protocol` varchar(150) NOT NULL,
    `PortNum` integer NOT NULL,
    `VulnString` longtext NOT NULL,
    `FixString` longtext NOT NULL
)
;
CREATE TABLE `TextVulns` (
    `tvid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ScriptID` varchar(300) NOT NULL,
    `public_id` varchar(20) NOT NULL,
    `MatchString` varchar(600) NOT NULL,
    `VulnString` longtext NOT NULL,
    `FixString` longtext NOT NULL,
    `risk_level` smallint UNSIGNED NOT NULL
)
;
CREATE TABLE `hosts` (
    `hid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `sid` integer NOT NULL,
    `ip4` longtext NOT NULL,
    `hostname` longtext NOT NULL,
    `status` longtext NOT NULL,
    `mac` longtext NOT NULL,
    `distance` integer,
    `uptime` longtext NOT NULL,
    `upstr` longtext NOT NULL
)
;
CREATE TABLE `os` (
    `oid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `hid` integer NOT NULL,
    `name` longtext NOT NULL,
    `family` longtext NOT NULL,
    `generation` longtext NOT NULL,
    `type` longtext NOT NULL,
    `vendor` longtext NOT NULL
)
;
ALTER TABLE `os` ADD CONSTRAINT `hid_refs_hid_92faf113` FOREIGN KEY (`hid`) REFERENCES `hosts` (`hid`);
CREATE TABLE `ports` (
    `pid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `hid` integer NOT NULL,
    `port` integer,
    `state` longtext NOT NULL,
    `name` longtext NOT NULL,
    `product` longtext NOT NULL,
    `version` longtext NOT NULL,
    `extra` longtext NOT NULL,
    `proto` longtext NOT NULL,
    `fingerprint` longtext NOT NULL
)
;
ALTER TABLE `ports` ADD CONSTRAINT `hid_refs_hid_24b2b22a` FOREIGN KEY (`hid`) REFERENCES `hosts` (`hid`);
CREATE TABLE `scans` (
    `sid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userId` integer NOT NULL,
    `subscription_level` integer,
    `version` longtext NOT NULL,
    `args` longtext NOT NULL,
    `starttime` datetime,
    `endtime` datetime
)
;
ALTER TABLE `scans` ADD CONSTRAINT `userId_refs_id_dcc46e37` FOREIGN KEY (`userId`) REFERENCES `auth_user` (`id`);
ALTER TABLE `hosts` ADD CONSTRAINT `sid_refs_sid_9b4ade76` FOREIGN KEY (`sid`) REFERENCES `scans` (`sid`);
CREATE TABLE `vulns` (
    `vid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `hid` integer NOT NULL,
    `tvid` integer NOT NULL
)
;
ALTER TABLE `vulns` ADD CONSTRAINT `hid_refs_hid_dc1cab26` FOREIGN KEY (`hid`) REFERENCES `hosts` (`hid`);
ALTER TABLE `vulns` ADD CONSTRAINT `tvid_refs_tvid_2d413f24` FOREIGN KEY (`tvid`) REFERENCES `TextVulns` (`tvid`);
CREATE INDEX `TextVulns_7914e307` ON `TextVulns` (`ScriptID`);
CREATE INDEX `hosts_236a1d8` ON `hosts` (`sid`);
CREATE INDEX `os_3f16467f` ON `os` (`hid`);
CREATE INDEX `ports_3f16467f` ON `ports` (`hid`);
CREATE INDEX `scans_bb972757` ON `scans` (`userId`);
CREATE INDEX `vulns_3f16467f` ON `vulns` (`hid`);
CREATE INDEX `vulns_f634e4ee` ON `vulns` (`tvid`);
COMMIT;
