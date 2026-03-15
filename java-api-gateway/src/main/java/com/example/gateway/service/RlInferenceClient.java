package com.example.gateway.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Service client for communicating with the RL Inference Service.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RlInferenceClient {

    private final RestTemplate restTemplate;

    @Value("${rl.inference.service.url:http://localhost:8000/predict_action}")
    private String inferenceServiceUrl;

    @Value("${rl.inference.service.timeout:10000}")
    private int serviceTimeout;

    /**
     * Predict action for given observation data.
     *
     * @param observationData List of observation values
     * @return Predicted action as integer
     * @throws RlInferenceException if prediction fails
     */
    public int predictAction(List<Double> observationData) {
        try {
            log.info("Sending prediction request with {} observations to {}", 
                    observationData.size(), inferenceServiceUrl);

            // Create request payload
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("obs_data", observationData);

            // Make HTTP POST request
            PredictionResponse response = restTemplate.postForObject(
                    inferenceServiceUrl,
                    requestBody,
                    PredictionResponse.class
            );

            if (response == null) {
                log.error("Received null response from inference service");
                throw new RlInferenceException("Received null response from inference service");
            }

            log.info("Predicted action: {}", response.getAction());
            return response.getAction();

        } catch (HttpClientErrorException e) {
            log.error("HTTP error from inference service: {} - {}", 
                    e.getStatusCode(), e.getResponseBodyAsString());
            throw new RlInferenceException(
                    String.format("HTTP %d error from inference service: %s",
                            e.getStatusCode().value(), e.getResponseBodyAsString()),
                    e
            );
        } catch (ResourceAccessException e) {
            log.error("Connection error to inference service at {}: {}", 
                    inferenceServiceUrl, e.getMessage());
            throw new RlInferenceException(
                    String.format("Failed to connect to inference service at %s: %s",
                            inferenceServiceUrl, e.getMessage()),
                    e
            );
        } catch (Exception e) {
            log.error("Unexpected error during prediction: {}", e.getMessage(), e);
            throw new RlInferenceException(
                    String.format("Unexpected error during prediction: %s", e.getMessage()),
                    e
            );
        }
    }

    /**
     * Check health of the inference service.
     *
     * @return true if service is healthy, false otherwise
     */
    public boolean isServiceHealthy() {
        try {
            String healthUrl = inferenceServiceUrl.replace("/predict_action", "/health");
            HealthResponse response = restTemplate.getForObject(
                    healthUrl,
                    HealthResponse.class
            );
            return response != null && "healthy".equals(response.getStatus());
        } catch (Exception e) {
            log.warn("Inference service health check failed: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Custom exception for RL Inference errors.
     */
    public static class RlInferenceException extends RuntimeException {
        public RlInferenceException(String message) {
            super(message);
        }

        public RlInferenceException(String message, Throwable cause) {
            super(message, cause);
        }
    }

    /**
     * Response model for predictions.
     */
    @lombok.Data
    @lombok.NoArgsConstructor
    @lombok.AllArgsConstructor
    public static class PredictionResponse {
        private int action;
        private Double confidence;
    }

    /**
     * Response model for health check.
     */
    @lombok.Data
    @lombok.NoArgsConstructor
    @lombok.AllArgsConstructor
    public static class HealthResponse {
        private String status;
        private boolean modelLoaded;
        private String modelPath;
    }
}
