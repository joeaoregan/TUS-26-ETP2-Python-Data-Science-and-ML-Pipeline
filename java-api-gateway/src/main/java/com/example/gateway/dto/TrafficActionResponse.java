package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Response containing predicted traffic signal action")
public class TrafficActionResponse {

    @Schema(description = "Predicted action index from RL model", example = "2")
    private int predictedAction;

    @Schema(description = "Human-readable traffic signal state", example = "GREEN")
//    private String signalState;
    private TrafficSignalState signalState;

    @Schema(description = "Unix timestamp of prediction", example = "1710000000000")
    private long timestamp;

    @Schema(description = "Status of the request", example = "success")
    private String status;
}
