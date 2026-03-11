# Domain References

The initial pesticide and fertilizer item fields in this starter are based on these references:

- U.S. EPA pesticide label basics: registration number, active ingredients, signal words, storage/disposal, and use directions.
- OSHA Hazard Communication / SDS expectations for hazardous materials handling metadata.
- State fertilizer labeling guidance commonly requiring grade (N-P-K), guaranteed analysis, net weight, and registrant/manufacturer details.

These references drove the following model fields:

- Pesticides: `epa_registration_number`, `active_ingredient`, `signal_word`, `restricted_use`, `reentry_interval_hours`, `sds_url`
- Fertilizers: `npk_grade`, `guaranteed_analysis`, `slow_release`, `coverage_area_sq_m`
- Shared inventory controls: `lot_code`, `expiration_date`, `storage_location`, `unit_of_measure`, `on_hand_quantity`
