use aivs;

DROP TABLE IF EXISTS TextVulns;
CREATE TABLE IF NOT EXISTS TextVulns (
    tvid INT(10) NOT NULL AUTO_INCREMENT,
	ScriptID VARCHAR(100) NOT NULL,
	MatchString VARCHAR(200) NOT NULL,
	VulnString TEXT,
	FixString TEXT,
	CONSTRAINT pk_TextVulns_tvid PRIMARY KEY (tvid)
); 

DROP TABLE IF EXISTS PortVuns;
CREATE TABLE IF NOT EXISTS PortVulns (
	pvid INT(10) NOT NULL AUTO_INCREMENT,
	Protocol VARCHAR(50) NOT NULL,
	PortNum INTEGER NOT NULL,
	VulnString TEXT,
	FixString TEXT,
	CONSTRAINT pk_PortVulns_pvid PRIMARY KEY (pvid)
);

INSERT INTO TextVulns (ScriptID, MatchString) values ("smb-check-vulns", "MS08-067: VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smb-check-vulns", "Conficker: Likely INFECTED");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smb-check-vulns", "regsvc DoS: VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smb-check-vulns", "SMBv2 DoS (CVE-2009-3103): VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smb-check-vulns", "MS06-025: VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smb-check-vulns", "MS07-029: VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smtp-vuln-cve2010-4344", "Exim (CVE-2010-4344): VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smtp-vuln-cve2010-4344", "Exim (CVE-2010-4345): VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smtp-vuln-cve2011-1720", "State: VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("smtp-vuln-cve2011-1764", "State: VULNERABLE");
INSERT INTO TextVulns (ScriptID, MatchString) values ("ssl-known-key", "is in the database");
INSERT INTO TextVulns (ScriptID, MatchString) values ("wdb-version", "VULNERABLE: Wind River");
COMMIT;
