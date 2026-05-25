FROM kalilinux/kali-rolling

# Pre-configure network testing tools and brute-forcers
RUN apt-get update && apt-get install -y hydra curl iputils-ping

# Keep the container alive in the background so we can execute attacks manually
CMD ["tail", "-f", "/dev/null"]