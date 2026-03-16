package com.example.gateway.config;

import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.OpenAPI;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Value("${api.title}")
    private String apiTitle;

    @Value("${api.description}")
    private String apiDescription;

    @Value("${api.version}")
    private String apiVersion;

	@Bean
	OpenAPI trafficControlApi() {
		return new OpenAPI().info(new Info().title(apiTitle)
				.description(apiDescription).version(apiVersion));
	}
}
