Feature: Visualize data
  Visualize data as graphs.

  Scenario: Create graph of raw EEG data
    Given a time series of raw EEG data.
    When I plot this data
    Then a line plot is generated.


