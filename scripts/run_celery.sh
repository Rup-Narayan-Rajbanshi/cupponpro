#!/usr/bin/env bash
celery -A project worker -B -l info
