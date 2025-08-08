import subprocess
import time
from pyngrok import ngrok

def start_streamlit_with_ngrok():
    """启动Streamlit应用并通过ngrok创建公网链接"""
    
    print("🚀 启动小微企业信贷评分系统...")
    
    # 启动Streamlit应用
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待应用启动
    time.sleep(5)
    
    try:
        # 创建ngrok隧道
        print("🌐 创建公网链接...")
        public_url = ngrok.connect(8501)
        
        print("✅ 部署成功！")
        print(f"📱 公网访问链接: {public_url}")
        print("🔗 本地访问链接: http://localhost:8501")
        print("\n💡 提示:")
        print("- 按 Ctrl+C 停止服务")
        print("- 链接会在程序关闭后失效")
        print("- 建议使用Streamlit Cloud进行永久部署")
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在停止服务...")
            
    except Exception as e:
        print(f"❌ 创建公网链接失败: {e}")
    finally:
        # 清理资源
        ngrok.kill()
        streamlit_process.terminate()
        print("✅ 服务已停止")

if __name__ == "__main__":
    start_streamlit_with_ngrok()
