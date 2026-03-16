package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Health check response")
public class HealthResponse {

    @Schema(description = "Overall service status", example = "healthy")
    private String status;

    @Schema(description = "Inference service status", example = "up")
    private String inferenceService;

    @Schema(description = "Unix timestamp", example = "1710000000000")
    private long timestamp;
}
