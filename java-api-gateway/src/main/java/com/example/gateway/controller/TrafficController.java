package com.example.gateway.controller;

import com.example.gateway.service.RlInferenceClient;
import com.example.gateway.service.RlInferenceClient.RlInferenceException;

import io.swagger.v3.oas.annotations.Operation;
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

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * REST Controller for traffic signal control.
 */
@Slf4j
@RestController
@RequestMapping("/api/traffic")
@RequiredArgsConstructor
@Tag(name = "Traffic Control API", description = "Endpoints for traffic signal prediction and health monitoring")
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
	@Operation(summary = "Get predicted traffic signal action", description = "Generates dummy observations and returns the predicted traffic signal state.")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully", content = @Content(mediaType = "application/json", schema = @Schema(example = """
			    {
			      "predictedAction": 2,
			      "signalState": "GREEN",
			      "timestamp": 1710000000000,
			      "status": "success"
			    }
			""")))
	@ApiResponse(responseCode = "503", description = "Inference service unavailable")
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error")
	@GetMapping("/action")
	public ResponseEntity<Map<String, Object>> getTrafficAction() {
		try {
			log.info("Received request for traffic action prediction");

			// Generate dummy observation data (10 features)
			// In a real scenario, these would come from actual traffic sensors
			List<Double> observationData = generateDummyObservations(observationDimension);
			log.debug("Generated observation data: {}", observationData);

			// Get prediction from RL model
			int predictedAction = rlInferenceClient.predictAction(observationData);

			// Map action to traffic signal state
			String trafficSignalState = mapActionToSignalState(predictedAction);

			Map<String, Object> response = new HashMap<>();
			response.put("predictedAction", predictedAction);
			response.put("signalState", trafficSignalState);
			response.put("timestamp", System.currentTimeMillis());
			response.put("status", "success");

			log.info("Successfully generated traffic action: {} ({})", predictedAction, trafficSignalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException e) {
			log.error("Failed to get traffic action: {}", e.getMessage());
			return buildErrorResponse("Inference service error: " + e.getMessage(), HttpStatus.SERVICE_UNAVAILABLE);

		} catch (Exception e) {
			log.error("Unexpected error getting traffic action", e);
			return buildErrorResponse("Internal server error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Get traffic action with custom observation data.
	 *
	 * @param request Request containing observation data
	 * @return ResponseEntity with predicted action
	 */
	@Operation(summary = "Predict traffic signal action using custom observations", description = "Accepts a list of observation values and returns the predicted traffic signal state.")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully", content = @Content(mediaType = "application/json", schema = @Schema(example = """
			    {
			      "predictedAction": 1,
			      "signalState": "YELLOW",
			      "timestamp": 1710000000000,
			      "status": "success"
			    }
			""")))
	@ApiResponse(responseCode = "400", description = "Invalid observation data")
	@ApiResponse(responseCode = "503", description = "Inference service unavailable")
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error")
	@PostMapping("/action")
	public ResponseEntity<Map<String, Object>> predictTrafficAction(@RequestBody TrafficActionRequest request) {
		try {
			log.info("Received custom traffic action request with {} observations", request.getObservations().size());

			// Validate observation data
			if (request.getObservations() == null || request.getObservations().isEmpty()) {
				return buildErrorResponse("Observations data is required", HttpStatus.BAD_REQUEST);
			}

			if (request.getObservations().size() != observationDimension) {
				return buildErrorResponse(String.format("Expected %d observations but received %d",
						observationDimension, request.getObservations().size()), HttpStatus.BAD_REQUEST);
			}

			// Get prediction from RL model
			int predictedAction = rlInferenceClient.predictAction(request.getObservations());

			// Map action to traffic signal state
			String trafficSignalState = mapActionToSignalState(predictedAction);

			Map<String, Object> response = new HashMap<>();
			response.put("predictedAction", predictedAction);
			response.put("signalState", trafficSignalState);
			response.put("timestamp", System.currentTimeMillis());
			response.put("status", "success");

			log.info("Successfully predicted traffic action: {} ({})", predictedAction, trafficSignalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException e) {
			log.error("Failed to predict traffic action: {}", e.getMessage());
			return buildErrorResponse("Inference service error: " + e.getMessage(), HttpStatus.SERVICE_UNAVAILABLE);

		} catch (Exception e) {
			log.error("Unexpected error predicting traffic action", e);
			return buildErrorResponse("Internal server error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Health check endpoint.
	 *
	 * @return ResponseEntity with health status
	 */
	@Operation(summary = "Health check", description = "Checks whether the RL inference service is reachable and responding.")
	@ApiResponse(responseCode = "200", description = "Service is healthy", content = @Content(mediaType = "application/json", schema = @Schema(example = """
			    {
			      "status": "healthy",
			      "inferenceService": "up",
			      "timestamp": 1710000000000
			    }
			""")))
	@GetMapping("/health")
	public ResponseEntity<Map<String, Object>> healthCheck() {
		Map<String, Object> health = new HashMap<>();

		try {
			boolean inferenceServiceHealthy = rlInferenceClient.isServiceHealthy();

			health.put("status", inferenceServiceHealthy ? "healthy" : "degraded");
			health.put("inferenceService", inferenceServiceHealthy ? "up" : "down");
			health.put("timestamp", System.currentTimeMillis());

			HttpStatus status = inferenceServiceHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE;
			return new ResponseEntity<>(health, status);

		} catch (Exception e) {
			log.warn("Health check failed: {}", e.getMessage());
			health.put("status", "unhealthy");
			health.put("error", e.getMessage());
			health.put("timestamp", System.currentTimeMillis());
			return new ResponseEntity<>(health, HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Generate dummy observation data for testing. In production, this would be
	 * replaced with actual sensor data.
	 *
	 * @param size Number of features needed
	 * @return List of observation values
	 */
	private List<Double> generateDummyObservations(int size) {
		List<Double> observations = new java.util.ArrayList<>();
		for (int i = 0; i < size; i++) {
			// Generate values between 0 and 1 (normalized traffic metrics)
			observations.add(random.nextDouble());
		}
		return observations;
	}

	/**
	 * Map RL action to human-readable traffic signal state.
	 *
	 * @param action The action value from RL model
	 * @return Human-readable signal state
	 */
	private String mapActionToSignalState(int action) {
		return switch (action) {
		case 0 -> "RED";
		case 1 -> "YELLOW";
		case 2 -> "GREEN";
		case 3 -> "GREEN_EXTENDED";
		default -> "UNKNOWN";
		};
	}

	/**
	 * Build error response.
	 *
	 * @param message Error message
	 * @param status  HTTP status
	 * @return ResponseEntity with error details
	 */
	private ResponseEntity<Map<String, Object>> buildErrorResponse(String message, HttpStatus status) {
		Map<String, Object> errorResponse = new HashMap<>();
		errorResponse.put("status", "error");
		errorResponse.put("message", message);
		errorResponse.put("timestamp", System.currentTimeMillis());
		return new ResponseEntity<>(errorResponse, status);
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
