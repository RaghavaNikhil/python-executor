FROM python:3.11-slim AS builder

# Install everything needed to build nsjail
RUN apt-get update && apt-get install -y \
    git \
    clang \
    make \
    g++ \
    flex \
    bison \
    pkg-config \
    protobuf-compiler \
    libprotobuf-dev \
    libnl-route-3-dev \
    libcap-dev \
    libseccomp-dev \
    && apt-get clean

# Clone and build nsjail
RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && make && cp nsjail /usr/local/bin/

# Final stage
FROM python:3.11-slim

# Install runtime libraries only (needed for nsjail)
RUN apt-get update && apt-get install -y \
    libprotobuf32 \
    libnl-route-3-200 \
    libcap2 \
    libseccomp2 && \
    apt-get clean

# Copy nsjail binary from builder
COPY --from=builder /usr/local/bin/nsjail /usr/local/bin/nsjail

# Install Python dependencies
RUN pip install flask==2.3.3 pandas numpy

# Copy app files
WORKDIR /app
COPY . .

# Create a new user and switch to it
RUN useradd -m appuser
USER appuser

# Make sure /tmp is writable
# RUN mkdir -p /tmp && chmod 777 /tmp

EXPOSE 8080
CMD ["python", "main.py"]
