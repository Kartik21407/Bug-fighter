package com.circularcarbon.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.Arrays;

@Configuration
public class WebConfig {

    @Value("${cors.allowed-origins:http://localhost:5173,http://localhost:3000,http://localhost:80,http://localhost:8081,http://frontend:80}")
    private String allowedOrigins;

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                String[] origins = Arrays.stream(allowedOrigins.split(","))
                        .map(String::trim)
                        .filter(s -> !s.isEmpty())
                        .toArray(String[]::new);

                boolean containsWildcard = Arrays.stream(origins).anyMatch(o -> o.equals("*") || o.contains("*"));

                if (containsWildcard) {
                    registry.addMapping("/**")
                            .allowedOriginPatterns(origins)
                            .allowedMethods("*")
                            .allowedHeaders("*")
                            .allowCredentials(false);
                } else {
                    registry.addMapping("/**")
                            .allowedOrigins(origins)
                            .allowedMethods("*")
                            .allowedHeaders("*");
                }
            }
        };
    }
}
