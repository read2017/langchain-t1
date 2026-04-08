import asyncio
import time

async def boil_water():
    print("【烧水】开始烧水... (模拟耗时 API 调用)")
    # await 会挂起当前任务，把 CPU 控制权还给主循环
    await asyncio.sleep(3) 
    print("【烧水】水开了！")
    return "热水"

async def chop_vegetables():
    for i in range(1, 4):
        print(f"【切菜】正在切第 {i} 棵白菜...")
        # 模拟切菜也需要一点点时间
        await asyncio.sleep(0.5)
    print("【切菜】菜切完了！")

async def main():
    start_time = time.perf_counter()
    print("--- 晚餐准备启动 ---")

    # 同时运行两个任务
    # 程序走到这里时，烧水任务开始执行，遇到 await 后立即切换到切菜任务
    await asyncio.gather(boil_water(), chop_vegetables())

    end_time = time.perf_counter()
    print(f"--- 晚餐准备好了！总耗时: {end_time - start_time:.2f} 秒 ---")

if __name__ == "__main__":
    asyncio.run(main())