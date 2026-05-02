#!/bin/zsh
# AIWF v13.0.0 OMEGA CLI Wrapper

COMMAND=$1
shift
ARGS=$@

case $COMMAND in
    "/plan")
        python3 factory/scripts/automation/plan_content.py $ARGS
        ;;
    "/create")
        python3 factory/scripts/core/compose.py $ARGS
        ;;
    "/dev")
        python3 factory/core/runner.py $ARGS
        ;;
    "/audit")
        python3 factory/scripts/maintenance/health_scorer.py $ARGS
        ;;
    "/git")
        # Route to security sentinel if flags are present
        if [[ "$*" == *"--security-fix"* ]] || [[ "$*" == *"--action-fix"* ]]; then
            python3 factory/core/security_sentinel.py --action fix --path .
        else
            python3 factory/scripts/core/omega_release.py $ARGS
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
    "/chaos")
        python3 factory/core/scaling_engine.py $ARGS
        ;;
    "/health")
        python3 factory/core/health_dashboard.py $ARGS
        ;;
    "/gate")
        python3 factory/core/omega_gate.py $ARGS
        ;;
    "/guide")
        python3 factory/scripts/core/swarm.py $ARGS
        ;;
    "/help")
        echo "AIWF commands:"
        echo "  /plan      /create    /dev      /audit"
        echo "  /git       /deploy    /revenue  /sync"
        echo "  /master    /chaos     /health   /gate"
        echo "  /guide     /help"
        echo ""
        echo "Examples:"
        echo "  /plan phase-02/agent-router"
        echo "  /create spec --type api"
        echo "  /git --security-fix"
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Usage: /plan, /create, /dev, /audit, /git, /deploy, /revenue, /sync, /master, /chaos, /health, /gate, /guide, /help"
        ;;
esac
