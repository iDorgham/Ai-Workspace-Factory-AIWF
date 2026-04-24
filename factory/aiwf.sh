#!/bin/zsh
# AIWF v13.0.0 OMEGA CLI Wrapper

COMMAND=$1
shift
ARGS=$@

case $COMMAND in
    "/plan")
        python3 factory/scripts/plan_content.py $ARGS
        ;;
    "/create")
        python3 factory/scripts/compose.py $ARGS
        ;;
    "/dev")
        python3 factory/core/runner.py $ARGS
        ;;
    "/audit")
        python3 factory/scripts/health_scorer.py $ARGS
        ;;
    "/git")
        # Route to security sentinel if flags are present
        if [[ "$*" == *"--security-fix"* ]] || [[ "$*" == *"--action-fix"* ]]; then
            python3 factory/core/security_sentinel.py --action fix --path .
        else
            python3 factory/scripts/omega_release.py $ARGS
        fi
        ;;
    "/deploy")
        python3 factory/core/deploy_engine.py $ARGS
        ;;
    "/revenue")
        python3 factory/core/revenue_engine.py $ARGS
        ;;
    "/sync")
        python3 factory/core/neural_fabric.py $ARGS
        ;;
    "/master")
        # Route to evolution engine
        if [[ "$*" == *"learn"* ]]; then
            python3 factory/core/evolution_engine.py --action learn
        elif [[ "$*" == *"evolve"* ]]; then
            # Extract pattern ID from ARGS (simplified for wrapper)
            python3 factory/core/evolution_engine.py --action evolve --pattern "auto-shard-provisioning"
        fi
        ;;
    "/guide")
        python3 factory/scripts/swarm.py $ARGS
        ;;
    "/help")
        cat docs/context/system-prompt.md
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Usage: /plan, /create, /dev, /audit, /git, /guide, /help"
        ;;
esac
