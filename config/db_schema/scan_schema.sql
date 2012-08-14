use aivs;

DROP TABLE IF EXISTS scans;
CREATE TABLE IF NOT EXISTS scans (
    sid INT(10) NOT NULL AUTO_INCREMENT,
    userId INT(10) NOT NULL,
    subscription_level int,
    version TEXT,
    xmlversion TEXT,
    args TEXT,
    types TEXT,
    starttime DATETIME,
    startstr TEXT,
    endtime DATETIME,
    endstr TEXT,
    numservices INTEGER,
    CONSTRAINT pk_scans_sid PRIMARY KEY (sid)
);

ALTER TABLE `scans` ADD CONSTRAINT `userId_refs_id` FOREIGN KEY (`userId`) REFERENCES `auth_user` (`id`);


DROP TABLE IF EXISTS hosts;
CREATE TABLE IF NOT EXISTS hosts (
    hid INT(10) NOT NULL AUTO_INCREMENT,
    sid INTEGER NOT NULL,
    ip4 TEXT,
    ip4num INTEGER,
    hostname TEXT,
    status TEXT,
    tcpcount INTEGER,
    udpcount INTEGER,
    mac TEXT,
    vendor TEXT,
    ip6 TEXT,
    distance INTEGER,
    uptime TEXT,
    upstr TEXT,
    CONSTRAINT pk_hosts_hid PRIMARY KEY (hid),
    CONSTRAINT fk_hosts_sid FOREIGN KEY (sid) REFERENCES scans(sid)
);

DROP TABLE IF EXISTS sequencing;
CREATE TABLE IF NOT EXISTS sequencing (
    sqid INT(10) NOT NULL AUTO_INCREMENT,
    hid INT(10) NOT NULL,
    tcpclass TEXT,
    tcpindex TEXT,
    tcpvalues TEXT,
    ipclass TEXT,
    ipvalues TEXT,
    tcptclass TEXT,
    tcptvalues TEXT,
    CONSTRAINT pk_sequencing_sqid PRIMARY KEY (sqid),
    CONSTRAINT fk_sequencing_hid FOREIGN KEY (hid) REFERENCES hosts(hid)
);

DROP TABLE IF EXISTS ports;
CREATE TABLE IF NOT EXISTS ports (
    pid INT(10) NOT NULL AUTO_INCREMENT,
    hid INT(10) NOT NULL,
    port INTEGER,
    type TEXT,
    state TEXT,
    name TEXT,
    tunnel TEXT,
    product TEXT,
    version TEXT,
    extra TEXT,
    confidence INTEGER,
    method TEXT,
    proto TEXT,
    owner TEXT,
    rpcnum TEXT,
    fingerprint TEXT,
    CONSTRAINT pk_ports_pid PRIMARY KEY (pid),
    CONSTRAINT fk_ports_hid FOREIGN KEY (hid) REFERENCES hosts(hid)
);

DROP TABLE IF EXISTS os;
CREATE TABLE IF NOT EXISTS os (
    oid INT(10) NOT NULL AUTO_INCREMENT,
    hid INT(10) NOT NULL,
    name TEXT,
    family TEXT,
    generation TEXT,
    type TEXT,
    vendor TEXT,
    accuracy INTEGER,
    CONSTRAINT pk_os_oid PRIMARY KEY (oid),
    CONSTRAINT fk_os_hid FOREIGN KEY (hid) REFERENCES hosts(hid)
);

DROP TABLE IF EXISTS vulns;
CREATE TABLE IF NOT EXISTS vulns (
	vid INT(10) NOT NULL AUTO_INCREMENT,
	hid INT(10) NOT NULL,
	tvid INT(10) NOT NULL,
	CONSTRAINT pk_vulns_vid PRIMARY KEY (vid),
	CONSTRAINT fk_vuln_hid FOREIGN KEY (hid) REFERENCES hosts(hid),
	CONSTRAINT fk_vuln_tvid FOREIGN KEY (tvid) REFERENCES TextVulns(tvid)
);

