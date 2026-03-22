package com.example.gateway.controller;

import com.example.gateway.dto.ErrorResponse;
import com.example.gateway.dto.HealthResponse;
import com.example.gateway.dto.TrafficActionResponse;
import com.example.gateway.dto.TrafficSignalState;
import com.example.gateway.service.RlInferenceClient;
import com.example.gateway.service.RlInferenceClient.RlInferenceException;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Random;

/**
 * REST Controller for traffic signal control.
 */
@Slf4j
@RestController
@RequestMapping("/api/traffic")
@RequiredArgsConstructor
//@Tag(name = "Traffic Control API", description = "Endpoints for traffic signal prediction and health monitoring")
public class TrafficController {

	private final RlInferenceClient rlInferenceClient;
	private static final Random random = new Random();

	@Value("${rl.inference.observation-dimension:9}")
	private int observationDimension;

	/**
	 * Get predicted action for traffic signal control.
	 *
	 * @return ResponseEntity with predicted action
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "getTrafficAction", summary = "Get predicted traffic signal action", description = "Generates dummy observations and returns the predicted traffic signal state.")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully", content = @Content(mediaType = "application/json", schema = @Schema(example = """
			    {
			      "predictedAction": 2,
			      "signalState": "GREEN",
			      "timestamp": 1710000000000,
			      "status": "success"
			    }
			""")))
	@ApiResponse(responseCode = "503", description = "Inference service unavailable", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Inference service down", value = """
			{
			  "status": "error",
			  "message": "Inference service error: connection refused",
			  "timestamp": 1710000000000
			}
			""")))
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Internal server error", value = """
			{
			  "status": "error",
			  "message": "Internal server error: null pointer exception",
			  "timestamp": 1710000000000
			}
			""")))
	@GetMapping("/action")
	public ResponseEntity<?> getTrafficAction() {
		try {
			log.info("Received request for traffic action prediction");

			List<Double> observationData = generateDummyObservations(observationDimension);
			log.debug("Generated observation data: {}", observationData);

			int predictedAction = rlInferenceClient.predictAction(observationData);
			TrafficSignalState trafficSignalState = mapActionToSignalState(predictedAction);

			TrafficActionResponse response = new TrafficActionResponse(predictedAction, trafficSignalState,
					System.currentTimeMillis(), "success");

			log.info("Successfully generated traffic action: {} ({})", predictedAction, trafficSignalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException e) {
			log.error("Inference service unavailable, entering FALLBACK mode: {}", e.getMessage());

			// FALLBACK LOGIC: Instead of 503 error, return a safe default (e.g., Action 0 =
			// RED)
			int fallbackAction = 0;
			TrafficSignalState fallbackState = mapActionToSignalState(fallbackAction);

			TrafficActionResponse response = new TrafficActionResponse(fallbackAction, fallbackState,
					System.currentTimeMillis(), "fallback_mode (inference service down)");

			// Return 200 OK but with a "fallback" status in the JSON
			return ResponseEntity.ok(response);

		} catch (Exception e) {
			// Keep this as 500 because it's a code crash, not just a service being down
			log.error("Unexpected error", e);
			return buildErrorResponse("Internal server error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Get traffic action with custom observation data.
	 *
	 * @param request Request containing observation data
	 * @return ResponseEntity with predicted action
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "predictTrafficAction", summary = "Predict traffic signal action using custom observations", description = "Accepts a list of observation values and returns the predicted traffic signal state.")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully", content = @Content(mediaType = "application/json", schema = @Schema(example = """
			    {
			      "predictedAction": 1,
			      "signalState": "YELLOW",
			      "timestamp": 1710000000000,
			      "status": "success"
			    }
			""")))
	@ApiResponse(responseCode = "400", description = "Invalid observation data", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Invalid observation count", value = """
			{
			  "status": "error",
			  "message": "Expected 9 observations but received 3",
			  "timestamp": 1710000000000
			}
			""")))
	@ApiResponse(responseCode = "503", description = "Inference service unavailable", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Inference service down", value = """
			{
			  "status": "error",
			  "message": "Inference service error: timeout",
			  "timestamp": 1710000000000
			}
			""")))
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Internal server error", value = """
			{
			  "status": "error",
			  "message": "Internal server error: unexpected exception",
			  "timestamp": 1710000000000
			}
			""")))
	@PostMapping("/action")
	public ResponseEntity<?> predictTrafficAction(
			@io.swagger.v3.oas.annotations.parameters.RequestBody(description = "Custom observation values for prediction", required = true, content = @Content(mediaType = "application/json", examples = {
					@ExampleObject(name = "Typical morning traffic", value = """
							{
							  "observations": [0.12, 0.33, 0.41, 0.55, 0.62, 0.70, 0.81, 0.90, 0.95],
							  "metadata": "morning-peak"
							}
							"""), @ExampleObject(name = "Low congestion", value = """
							{
							  "observations": [0.05, 0.10, 0.08, 0.12, 0.15, 0.20, 0.18, 0.22, 0.25],
							  "metadata": "off-peak"
							}
							""") })) @RequestBody TrafficActionRequest request) {
		try {
			log.info("Received custom traffic action request with {} observations", request.getObservations().size());

			if (request.getObservations() == null || request.getObservations().isEmpty()) {
				return buildErrorResponse("Observations data is required", HttpStatus.BAD_REQUEST);
			}

			if (request.getObservations().size() != observationDimension) {
				return buildErrorResponse(String.format("Expected %d observations but received %d",
						observationDimension, request.getObservations().size()), HttpStatus.BAD_REQUEST);
			}

			int predictedAction = rlInferenceClient.predictAction(request.getObservations());
			TrafficSignalState trafficSignalState = mapActionToSignalState(predictedAction);

			TrafficActionResponse response = new TrafficActionResponse(predictedAction, trafficSignalState,
					System.currentTimeMillis(), "success");

			log.info("Successfully predicted traffic action: {} ({})", predictedAction, trafficSignalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException e) {
			log.error("Inference service unavailable, entering FALLBACK mode: {}", e.getMessage());

			// FALLBACK LOGIC: Instead of 503 error, return a safe default (e.g., Action 0 =
			// RED)
			int fallbackAction = 0;
			TrafficSignalState fallbackState = mapActionToSignalState(fallbackAction);

			TrafficActionResponse response = new TrafficActionResponse(fallbackAction, fallbackState,
					System.currentTimeMillis(), "fallback_mode (inference service down)");

			// Return 200 OK but with a "fallback" status in the JSON
			return ResponseEntity.ok(response);

		} catch (Exception e) {
			// Keep this as 500 because it's a code crash, not just a service being down
			log.error("Unexpected error", e);
			return buildErrorResponse("Internal server error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Health check endpoint.
	 *
	 * @return ResponseEntity with health status
	 */
	@Tag(name = "System Health")
	@Operation(operationId = "healthCheck", summary = "Health check", description = "Checks whether the RL inference service is reachable and responding.")
	@ApiResponse(responseCode = "200", description = "Service is healthy", content = @Content(mediaType = "application/json", schema = @Schema(example = """
			    {
			      "status": "healthy",
			      "inferenceService": "up",
			      "timestamp": 1710000000000
			    }
			""")))
	@ApiResponse(responseCode = "503", description = "Inference service degraded", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Service degraded", value = """
			{
			  "status": "degraded",
			  "inferenceService": "down",
			  "timestamp": 1710000000000
			}
			""")))
	@ApiResponse(responseCode = "500", description = "Health check failed", content = @Content(mediaType = "application/json", examples = @ExampleObject(name = "Health check error", value = """
			{
			  "status": "unhealthy",
			  "inferenceService": "down",
			  "timestamp": 1710000000000
			}
			""")))
	@GetMapping("/health")
	public ResponseEntity<?> healthCheck() {
		try {
			boolean inferenceServiceHealthy = rlInferenceClient.isServiceHealthy();

			HealthResponse response = new HealthResponse(inferenceServiceHealthy ? "healthy" : "degraded",
					inferenceServiceHealthy ? "up" : "down", System.currentTimeMillis());

			HttpStatus status = inferenceServiceHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE;
			return new ResponseEntity<>(response, status);

		} catch (Exception e) {
			log.warn("Health check failed: {}", e.getMessage());
			return new ResponseEntity<>(new HealthResponse("unhealthy", "down", System.currentTimeMillis()),
					HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	private List<Double> generateDummyObservations(int size) {
		List<Double> observations = new java.util.ArrayList<>();
		for (int i = 0; i < size; i++) {
			observations.add(random.nextDouble());
		}
		return observations;
	}

	private TrafficSignalState mapActionToSignalState(int action) {
		return switch (action) {
		case 0 -> TrafficSignalState.RED;
		case 1 -> TrafficSignalState.YELLOW;
		case 2 -> TrafficSignalState.GREEN;
		case 3 -> TrafficSignalState.GREEN_EXTENDED;
		default -> TrafficSignalState.UNKNOWN;
		};
	}

	private ResponseEntity<ErrorResponse> buildErrorResponse(String message, HttpStatus status) {
		return new ResponseEntity<>(new ErrorResponse("error", message, System.currentTimeMillis()), status);
	}

	/**
	 * Request model for custom traffic action prediction.
	 */
	@Schema(description = "Request body for custom traffic action prediction")
	@lombok.Data
	@lombok.NoArgsConstructor
	@lombok.AllArgsConstructor
	public static class TrafficActionRequest {

		@Schema(description = "List of observation values", example = "[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]")
		private List<Double> observations;

		@Schema(description = "Optional metadata for debugging or tracking", example = "peak-hour")
		private String metadata;
	}
}
