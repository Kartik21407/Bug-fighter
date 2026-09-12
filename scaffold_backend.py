import os

base_dir = r"c:\Users\Anuj\Desktop\HackOut\circular-carbon\backend"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write_file("pom.xml", """
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.4</version>
        <relativePath/>
    </parent>
    <groupId>com.circularcarbon</groupId>
    <artifactId>circular-carbon-backend</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>Circular Carbon Backend</name>
    <properties>
        <java.version>21</java.version>
    </properties>
    <dependencies>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
        <dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><scope>runtime</scope></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
        <dependency><groupId>org.springdoc</groupId><artifactId>springdoc-openapi-starter-webmvc-ui</artifactId><version>2.6.0</version></dependency>
    </dependencies>
    <build>
        <plugins><plugin><groupId>org.springframework.boot</groupId><artifactId>spring-boot-maven-plugin</artifactId></plugin></plugins>
    </build>
</project>
""")

write_file("src/main/resources/application.yml", """
server:
  port: 8080
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/circular_carbon
    username: postgres
    password: postgres
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui
""")

write_file("src/main/java/com/circularcarbon/CircularCarbonApplication.java", """
package com.circularcarbon;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class CircularCarbonApplication {
    public static void main(String[] args) { SpringApplication.run(CircularCarbonApplication.class, args); }
}
""")

write_file("src/main/java/com/circularcarbon/config/WebConfig.java", """
package com.circularcarbon.config;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
@Configuration
public class WebConfig {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/api/**").allowedOrigins("http://localhost:5173", "http://localhost:3000").allowedMethods("*").allowedHeaders("*");
            }
        };
    }
}
""")

write_file("src/main/java/com/circularcarbon/controller/HealthController.java", """
package com.circularcarbon.controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;
@RestController
public class HealthController {
    @GetMapping("/api/health")
    public Map<String, String> health() { return Map.of("status", "UP", "service", "circular-carbon-backend"); }
}
""")

print("Backend scaffolded.")
