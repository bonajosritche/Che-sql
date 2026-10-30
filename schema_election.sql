-- PROBLEMA:
-- Manwal ang botohan sa Student Election. Madaling madoble ang boto, hindi
-- malinaw ang tally, at matagal bago malaman kung sino ang panalo. May duda
-- rin kung tunay na isang boto lang ang bawat estudyante sa bawat posisyon.
--
-- SOLUSYON:
-- CLI system na may elections, positions, candidates, voters (masterlist), at
-- votes. Ang UNIQUE (election_id, voter_id, position_id) ang pumipigil sa
-- doble at maramihang boto. Ang tally ay COUNT() per candidate, may
-- percentage, winner detection, at voter turnout per grade level.

CREATE DATABASE IF NOT EXISTS school_election_db;
USE school_election_db;

CREATE TABLE IF NOT EXISTS elections (
  election_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(150) NOT NULL,
  school_year VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
  date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_el_status (status)
);

CREATE TABLE IF NOT EXISTS positions (
  position_id INT AUTO_INCREMENT PRIMARY KEY,
  election_id INT NOT NULL,
  position_name VARCHAR(80) NOT NULL,
  max_winners INT NOT NULL DEFAULT 1,
  display_order INT NOT NULL DEFAULT 1,
  CONSTRAINT fk_el_position FOREIGN KEY (election_id) REFERENCES elections(election_id) ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE KEY uniq_el_position_name (election_id, position_name)
);

CREATE TABLE IF NOT EXISTS candidates (
  candidate_id INT AUTO_INCREMENT PRIMARY KEY,
  position_id INT NOT NULL,
  full_name VARCHAR(150) NOT NULL,
  grade_level VARCHAR(20) NOT NULL,
  section VARCHAR(50) NOT NULL,
  party VARCHAR(80) DEFAULT NULL,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_el_candidate FOREIGN KEY (position_id) REFERENCES positions(position_id) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_el_candidate_position (position_id)
);

CREATE TABLE IF NOT EXISTS voters (
  voter_id VARCHAR(20) PRIMARY KEY,
  full_name VARCHAR(150) NOT NULL,
  grade_level VARCHAR(20) NOT NULL,
  section VARCHAR(50) NOT NULL,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS votes (
  vote_id INT AUTO_INCREMENT PRIMARY KEY,
  election_id INT NOT NULL,
  position_id INT NOT NULL,
  candidate_id INT NOT NULL,
  voter_id VARCHAR(20) NOT NULL,
  date_voted DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_el_v_election FOREIGN KEY (election_id) REFERENCES elections(election_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_el_v_position FOREIGN KEY (position_id) REFERENCES positions(position_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_el_v_candidate FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_el_v_voter FOREIGN KEY (voter_id) REFERENCES voters(voter_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  UNIQUE KEY uniq_el_vote_once (election_id, voter_id, position_id),
  INDEX idx_el_v_candidate (candidate_id)
);
