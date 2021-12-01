-- If the database handles table creations within transactions, do so.
BEGIN;

CREATE TABLE `ObservationError`(
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	observer ENUM('FLIGHTPLAN', 'TERMINAL', 'RADAR', 'IT') NOT NULL,
	observedAt timestamp NOT NULL,
	cause ENUM('ENDPOINT_UNAVAILABLE', 'ENDPOINT_UNRESPONSIVE', 'MALFORMED_RESPONSE', 'EXTRANEOUS_RESPONSE', 'INTERNAL_ERROR') NOT NULL,
	parameter text DEFAULT NULL
);

-- Use foreign key constraint instead of table inheritance, because MySQL is
-- lacking support for inheritance.

CREATE TABLE `ObservedEntry`(
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	observer ENUM('FLIGHTPLAN', 'TERMINAL', 'RADAR', 'IT') NOT NULL,
	observedAt timestamp NOT NULL,
	validUntil timestamp NOT NULL,
	outdated boolean NOT NULL DEFAULT FALSE,
	reported boolean NOT NULL DEFAULT FALSE,
	UNIQUE(id, observer)
);

CREATE TABLE `FlightplanEntry`(
	id int NOT NULL PRIMARY KEY,
	observer ENUM('FLIGHTPLAN', 'TERMINAL', 'RADAR', 'IT') GENERATED ALWAYS AS ('FLIGHTPLAN') STORED NOT NULL,
	callsign text NOT NULL,
	ssr text NOT NULL,
	rules text NOT NULL,
	aircraft text NOT NULL,
	wvc text NOT NULL,
	equipment text NOT NULL,
	origin text NOT NULL,
	eobt text NOT NULL,
	route text NOT NULL,
	destination text NOT NULL,
	eet int NOT NULL,
	eta timestamp NOT NULL,
	status text NOT NULL,
	registration text NOT NULL,
	icao4444 text NOT NULL
);

CREATE TABLE `TerminalEntry`(
	id int NOT NULL PRIMARY KEY,
	observer ENUM('FLIGHTPLAN', 'TERMINAL', 'RADAR', 'IT') GENERATED ALWAYS AS ('TERMINAL') STORED NOT NULL,
	level text NOT NULL,
	message text NOT NULL
);

CREATE TABLE `RadarEntry`(
	id int NOT NULL PRIMARY KEY,
	observer ENUM('FLIGHTPLAN', 'TERMINAL', 'RADAR', 'IT') GENERATED ALWAYS AS ('RADAR') STORED NOT NULL,
	callsign text NOT NULL,
	date timestamp NOT NULL,
	latitude double NOT NULL,
	altitude double NOT NULL
);

CREATE TABLE `ITEntry`(
	id int NOT NULL PRIMARY KEY,
	observer ENUM('FLIGHTPLAN', 'TERMINAL', 'RADAR', 'IT') GENERATED ALWAYS AS ('IT') STORED NOT NULL,
	name text NOT NULL,
	unit text NOT NULL,
	value text NOT NULL
);

ALTER TABLE `FlightplanEntry`
	ADD FOREIGN KEY (id, observer) REFERENCES `ObservedEntry`(id, observer);

ALTER TABLE `TerminalEntry`
	ADD FOREIGN KEY (id, observer) REFERENCES `ObservedEntry`(id, observer);

ALTER TABLE `RadarEntry`
	ADD FOREIGN KEY (id, observer) REFERENCES `ObservedEntry`(id, observer);

ALTER TABLE `ITEntry`
	ADD FOREIGN KEY (id, observer) REFERENCES `ObservedEntry`(id, observer);

-- User: tinf20cs1
GRANT SELECT
ON TABLE *
TO 'tinf20cs1'@'%';

-- User: fc
GRANT
	SELECT,
	INSERT
ON TABLE `ObservationError`
TO 'fc'@'%';

GRANT
	SELECT,
	INSERT,
	UPDATE (`validUntil`, `reported`, `outdated`)
ON TABLE `ObservedEntry`
TO 'fc'@'%';

GRANT
	SELECT,
	INSERT
ON TABLE `FlightplanEntry`
TO 'fc'@'%';

GRANT
	SELECT,
	INSERT
ON TABLE `TerminalEntry`
TO 'fc'@'%';

GRANT
	SELECT,
	INSERT
ON TABLE `RadarEntry`
TO 'fc'@'%';

GRANT
	SELECT,
	INSERT
ON TABLE `ITEntry`
TO 'fc'@'%';

-- User: alert
GRANT SELECT
ON TABLE `ObservationError`
TO 'alert'@'%';

GRANT SELECT
ON TABLE `ObservedEntry`
TO 'alert'@'%';

GRANT SELECT
ON TABLE `FlightplanEntry`
TO 'alert'@'%';

GRANT SELECT
ON TABLE `TerminalEntry`
TO 'alert'@'%';

GRANT SELECT
ON TABLE `RadarEntry`
TO 'alert'@'%';

GRANT SELECT
ON TABLE `ITEntry`
TO 'alert'@'%';

-- User: ui
GRANT SELECT
ON TABLE `ObservationError`
TO 'ui'@'%';

GRANT SELECT
ON TABLE `ObservedEntry`
TO 'ui'@'%';

GRANT SELECT
ON TABLE `FlightplanEntry`
TO 'ui'@'%';

GRANT SELECT
ON TABLE `TerminalEntry`
TO 'ui'@'%';

GRANT SELECT
ON TABLE `RadarEntry`
TO 'ui'@'%';

GRANT SELECT
ON TABLE `ITEntry`
TO 'ui'@'%';

FLUSH PRIVILEGES;

COMMIT;
