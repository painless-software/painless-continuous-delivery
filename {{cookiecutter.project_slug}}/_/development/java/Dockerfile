FROM openjdk:17-jdk-alpine as build

WORKDIR /workspace/app

COPY . .

RUN chmod +x mvnw \
 && ./mvnw install -DskipTests \
 && mkdir -p target/dependency \
 && cd target/dependency \
 && jar -xf ../*.jar

FROM openjdk:17-jdk-alpine

VOLUME /tmp

ARG DEPENDENCY=/workspace/app/target/dependency

COPY --from=build ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY --from=build ${DEPENDENCY}/META-INF /app/META-INF
COPY --from=build ${DEPENDENCY}/BOOT-INF/classes /app

ENTRYPOINT ["java", "-cp", "app:app/lib/*", "hello.Application"]
