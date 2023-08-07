## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Folder Structure](#folder-structure)
4. [Components and UI Elements](#components-and-ui-elements)
5. [Styling and Theming](#styling-and-theming)
6. [State Management](#state-management)
7. [Routing and Navigation](#routing-and-navigation)
8. [API Integration](#api-integration)
9. [User Authentication](#user-authentication)
10. [UI/UX Considerations](#uiux-considerations)
11. [Deployment](#deployment)
12. [Troubleshooting and Debugging](#troubleshooting-and-debugging)
13. [Additional Resources](#additional-resources)

## Introduction
Welcome to the frontend documentation for Sc2reporter! This section offers an overview of our frontend, highlighting its features, functionality, and technologies.

### Overview
Our frontend is the user interface of Sc2reporter, connecting users with the application's core features. It's designed for a seamless, engaging, and responsive user experience.

### Key Features

- Samples Page
- Sample Page
- Pangolin Page
- Nextclade page
- Variant page
- Dashboard page
- Users page

### Technologies

- **React:** Building dynamic interfaces efficiently.
- **React Router:** Seamless navigation and URL management.
- **TypeScript:** A typed superset of JavaScript that enhances code quality and maintainability.
- **Axios:** A popular HTTP client for making API requests and handling responses.
- **Ant Design (antd):** A comprehensive UI library for modern web applications.
- **Ant Design Charts:** An extension of Ant Design providing a wide range of charts for data visualization.
- **MSW (Mock Service Worker):** Simulating API responses for efficient frontend development and testing.

These technologies ensure a fast, reliable, and feature-rich frontend.

## Getting Started
   - Prerequisites for Frontend Development
   - Setting Up the Development Environment
   - Running the Frontend Locally

## Folder Structure
   - Explanation of Each Folder
   - Where to Find Components, Styles, Assets, etc.

## Components and UI Elements
   - Component Library Overview
   - List of Reusable Components
   - Props and Usage for Each Component

## Styling and Theming
   - CSS-in-JS Libraries Used
   - Styling Approaches (e.g., Styled Components, CSS Modules)
   - How to Apply Styles to Components
   - Theming and Customization Options

## State Management
   - State Handling in the Frontend
   - Integration with State Management Libraries (e.g., Redux, Context API)
   - Example of Managing State in Components

## Routing and Navigation
   - Setting Up Routes
   - Navigation Between Pages
   - Route Guards and Redirects

## API Integration
   - How Frontend Communicates with Backend APIs
   - Handling API Requests and Responses
   - Example Code for API Calls

## User Authentication
   - Authentication Flow and Components
   - Handling User Login and Registration
   - Securing Routes based on Authentication

## UI/UX Considerations
    - Design Principles and Guidelines
    - User Interaction Patterns
    - Responsive Design and Mobile Compatibility

## Deployment
    - Preparing Frontend for Production Build
    - Deploying the Frontend to Hosting Platforms
    - Integration with Backend Deployment

## Troubleshooting and Debugging
    - Common Frontend Issues and Solutions
    - Browser Developer Tools for Debugging

## Additional Resources
    - Links to UI/UX Guidelines
    - References for Styling and CSS-in-JS
    - Recommended Reading for Frontend Development

# Prefix URL Configuration
The prefix URL in this project is controlled by the environment variable \`REACT_APP_PREFIX_URL\`. By default, it is set to \`/\` to prevent any potential interference with Firebase hosting actions. When the project is run in production, the \`REACT_APP_PREFIX_URL\` variable can be configured with a different value as needed.
