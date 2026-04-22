School Management System (Biometrics & SMS Integration)

Overview

This project is a school management system composed of two integrated applications:

1. Biometrics Attendance System


2. SMS Communication System



It is designed to automate student attendance tracking using fingerprint devices and enable schools to send SMS notifications to students or groups via a SIM-based modem connected to a server.


---

1. Biometrics Attendance System

Description

The biometrics module integrates with a fingerprint device (ZKTeco-compatible) to record student attendance. It captures check-in and check-out data and synchronizes it with the server.

Features

Fingerprint-based student identification

Automatic check-in and check-out tracking

Stores student ID, name, and timestamp

Syncs data from biometric device to server

Attendance records stored in database


Workflow

1. Student scans fingerprint on the device


2. Device sends attendance logs to the server


3. Server processes data (check-in/check-out logic)


4. Records are stored under the corresponding student profile



Notes

Device integration is based on ZKTeco protocol

IP address of the device must be configured in the server settings



---

2. SMS Communication System

Description

The SMS module allows schools to send messages to students using a GSM modem with a SIM card. Messages can be sent individually or in bulk (groups/classes/clubs).

Features

Send SMS to a single student

Send bulk/group SMS (e.g., class, club, or batch)

SIM-based GSM modem integration

Server-controlled message dispatch


Workflow

1. School selects recipient(s) via web/app interface


2. Server receives SMS request


3. Server sends AT commands to GSM modem


4. Modem sends SMS using inserted SIM card




---

System Architecture

Backend Server: Handles biometrics processing + SMS routing

Biometric Device: Sends fingerprint logs to server

GSM Modem: Sends SMS messages via SIM card

Database: Stores student info, attendance, and messaging logs



---

Technologies Used

Backend: Python / Django

Database: SQL //to be changed to for real development PostgreSQL

Biometrics SDK: ZKTeco protocol integration

GSM Communication: AT Commands via serial/USB modem



---

Setup Requirements

Biometrics System

ZKTeco-compatible fingerprint device

Network connection between device and server

Configured device IP and port


SMS System

GSM modem with SIM card

Serial/USB connection to server machine

Active mobile network for SMS delivery



---

Key Module

sync.py → Handles biometric data synchronization

sms_service.py → Handles SMS sending via modem

student_model → Stores student information

Dailyattendance_model → Stores check-in/check-out logs

SMS_model -> stores messages status('pending', 'sent', 'failed)





