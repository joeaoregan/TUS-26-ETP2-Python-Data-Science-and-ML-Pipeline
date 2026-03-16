package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Error response model")
public class ErrorResponse {

    @Schema(description = "Status indicator", example = "error")
    private String status;

    @Schema(description = "Error message", example = "Inference service unavailable")
    private String message;

    @Schema(description = "Unix timestamp", example = "1710000000000")
    private long timestamp;
}
