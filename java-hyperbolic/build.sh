#!/bin/bash
# Java Swing Hyperbolic Tiling 빌드 및 실행 스크립트

echo "======================================================"
echo "Order-3 Heptagonal Tiling - Java Swing"
echo "======================================================"

# Maven이 설치되어 있는지 확인
if command -v mvn &> /dev/null; then
    echo "Maven을 사용하여 빌드합니다..."
    mvn clean package

    if [ $? -eq 0 ]; then
        echo ""
        echo "빌드 성공! 실행합니다..."
        echo ""
        java -jar target/hyperbolic-tiling.jar
    else
        echo "빌드 실패!"
        exit 1
    fi
else
    echo "Maven이 설치되어 있지 않습니다."
    echo "javac를 사용하여 컴파일합니다..."

    cd src/main/java
    javac hyperbolic/*.java

    if [ $? -eq 0 ]; then
        echo ""
        echo "컴파일 성공! 실행합니다..."
        echo ""
        java hyperbolic.HyperbolicViewer
    else
        echo "컴파일 실패!"
        exit 1
    fi
fi
