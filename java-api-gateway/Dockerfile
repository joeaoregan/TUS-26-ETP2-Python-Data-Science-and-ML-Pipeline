FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

COPY pom.xml .
# This layer is cached unless pom.xml changes
RUN mvn dependency:go-offline -B 

COPY src ./src
# Using -o (offline) makes the build faster if dependencies are already cached
RUN mvn clean package -DskipTests -o

# Runtime stage
FROM eclipse-temurin:17-jre-ubi9-minimal

WORKDIR /app

COPY --from=builder /build/target/traffic-gateway-*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
