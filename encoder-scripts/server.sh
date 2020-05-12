#!/bin/bash
#!/usr/local/bin/
#!/usr/bin/env
#!/usr/bin/ruby

export AWS_PROFILE=cloud
while true
do
    echo "POLLING FROM SQS"
    echo "Press [CTRL+C] to stop.."
    sleep 10
    python encoderJobChecker.py
done
