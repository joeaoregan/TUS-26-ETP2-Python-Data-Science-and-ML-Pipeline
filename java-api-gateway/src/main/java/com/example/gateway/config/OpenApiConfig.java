package com.example.gateway.config;

import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.OpenAPI;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

	@Bean
	OpenAPI trafficControlApi() {
		return new OpenAPI().info(new Info().title("AI Traffic Control API")
				.description("REST API Gateway for RL-based traffic signal control").version("1.0.0"));
	}
}
