package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Traffic signal state", enumAsRef = true)
public enum TrafficSignalState {
    RED,
    YELLOW,
    GREEN,
    GREEN_EXTENDED,
    UNKNOWN
}
