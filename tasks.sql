CREATE DATABASE TASKS;

USE TASKS;

CREATE TABLE tasks (
    SrNo INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    TasksCompletion DATETIME, 
    IsComplete VARCHAR(5), 
    TaskName VARCHAR(100), 
    TaskDescription VARCHAR(255),
    TaskType VARCHAR(100)    
);