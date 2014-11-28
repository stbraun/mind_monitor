Feature: Provide configuration.
  General settings shall be configurable.

  Scenario: Read database configuration.
    Given a configuration.
    When starting the application
    Then the configuration for the database is read.

  Scenario: Read preference for raw data.
    Given a configuration.
    When starting the application
    Then the preference for raw data is read.

