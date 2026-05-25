FROM ubuntu:latest

# Install SSH and the syslog daemon for auth.log generation
RUN apt-get update && apt-get install -y openssh-server rsyslog && \
    mkdir -p /run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Provision target accounts directly during the build phase
RUN useradd -m -s /bin/bash target1 && echo 'target1:password123' | chpasswd && \
    useradd -m -s /bin/bash admin_test && echo 'admin_test:admin' | chpasswd && \
    useradd -m -s /bin/bash sysops && echo 'sysops:qwerty' | chpasswd

EXPOSE 22

# Start the logging daemon natively, then SSH in the foreground
CMD /usr/sbin/rsyslogd && /usr/sbin/sshd -D