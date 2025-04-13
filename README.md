# OOP-Project
# Blood Donation Management System
## Overview 
The Blood Donation Management System is an application that helps manage donor registrations, blood inventory, and hospital requests efficiently. It ensures that blood donation centers can track available blood types, donor eligibility, and hospital requests in a structured manner. Users can register themselves writing their blood type and find suitable donors.

## Team Members
- Kanybekova Aiturgan(Leader and Presenter) - Oversees the project, ensures smooth progress, assigns tasks, and verifies final implementation.
- Askarbekova Meerim(Backend Developer) - Writes and manages the core logic, handles database operations, and ensures system functionality.
- Sarlykova Aiza(Designer) -  Designs the interface using PyQt Designer.
  
## Meetings and discussions documentation
https://docs.google.com/document/d/19o1r7gERA5ci_CQZ8dP_Uzb97aLcx-AnDkkrhUewomw/edit?tab=t.0

## Functions
- Donor Registration form (Add new donors with details like name, age, blood type, contact number, and location).
- Hospital Blood Request (Allow hospitals to request specific blood types).
- Blood Inventory Management (Maintains real-time records: if a new eligible donor registers, the corresponding blood quantity increases; if a hospital requests blood, the quantity decreases accordingly).
- Search and Match(Hospitals request a specific blood type they need and the app automatically finds a list of people with that type of blood).
- Message Notifications for Exceptions in Case of Wrong User Inputs(if the fields are not filled, the error message is seen).
- Graphical Blood Inventory dashboard(Display a bar chart showing available blood units per type using tools like Matplotlib or PyQtChart).
- Request Status Tracking (Allow status updates on blood requests (e.g., Pending, Fulfilled) and keep history for reporting).
- Database Integration (SQLite or MySQL) : Use DAO classes to perform Create, Read, Update, Delete (CRUD) operations on at least 3 tables:  Donors, BloodInventory, Requests.
- Information dashboard for better understanding of blood donation.
- Thank you message box after the user submits their registration form.

## Interface of the project
#### The main page 
<img width="421" alt="Снимок экрана 2025-04-12 в 15 38 31" src="https://github.com/user-attachments/assets/a0eb716d-6811-4fe0-b9a1-2d9c9861fd72" />

#### Table/chart
<img width="424" alt="Снимок экрана 2025-04-12 в 15 41 26" src="https://github.com/user-attachments/assets/59354d99-8184-43b2-bf90-8b6282bc4ed0" />
<img width="423" alt="Снимок экрана 2025-04-12 в 15 41 36" src="https://github.com/user-attachments/assets/756b0b82-55ea-41f5-a05f-4b44616dcd4f" />

#### About Us 
<img width="398" alt="Снимок экрана 2025-04-12 в 15 41 47" src="https://github.com/user-attachments/assets/c7e7e83e-b2e5-4bf1-bfd3-9298d5e9f46b" />

#### Preparation
<img width="404" alt="Снимок экрана 2025-04-12 в 15 41 59" src="https://github.com/user-attachments/assets/dc18d908-d2b1-4660-9023-c3a83a61dc23" />

#### Why it is Important?
<img width="401" alt="Снимок экрана 2025-04-12 в 15 42 09" src="https://github.com/user-attachments/assets/8c3550d4-fb98-436c-8fe0-6c8eee4b7c73" />

#### Who can Donate?
<img width="402" alt="Снимок экрана 2025-04-12 в 15 42 24" src="https://github.com/user-attachments/assets/216d544d-4214-45ed-a6b9-58c61e645c7e" />

#### Donate Blood Form
<img width="423" alt="Снимок экрана 2025-04-12 в 15 42 39" src="https://github.com/user-attachments/assets/27bbabf3-d477-4986-a951-003dc4a0884d" />

#### Request Blood Form 
<img width="422" alt="Снимок экрана 2025-04-12 в 15 42 55" src="https://github.com/user-attachments/assets/f39606fb-105d-47a8-a149-ebb67eac28bf" />

#### Errors 
<img width="420" alt="all_fields-must_be_filled" src="https://github.com/user-attachments/assets/0f929171-3b9d-4d18-9bff-57e482225907" />
<img width="421" alt="checkbox" src="https://github.com/user-attachments/assets/452c84a2-72e7-47bd-8af2-2da4357e2cfc" />

## Presentation

https://www.canva.com/design/DAGkH6EyEIs/drA0KINHbpGze1qG5RVKSQ/edit?utm_content=DAGkH6EyEIs&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton









