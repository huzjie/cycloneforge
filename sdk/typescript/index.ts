// cycloneforge TypeScript 客户端（浏览器 / Node 均可用）
export interface ForecastResponse {
  track: [number, number][];
  intensity: [number, number][];
  wind: number[][];
  n_steps: number;
}

export class CycloneClient {
  constructor(private baseUrl: string = "http://127.0.0.1:8000") {}

  async health(): Promise<{ status: string; version: string }> {
    return this.get<{ status: string; version: string }>("/health");
  }

  async forecast(
    features: number[],
    nSteps = 20,
    nMembers = 0,
    perturbScale = 0.1,
  ): Promise<ForecastResponse> {
    return this.post<ForecastResponse>("/v1/forecast", {
      features,
      n_steps: nSteps,
      n_members: nMembers,
      perturb_scale: perturbScale,
    });
  }

  private async get<T>(path: string): Promise<T> {
    const r = await fetch(this.baseUrl + path);
    return (await r.json()) as T;
  }

  private async post<T>(path: string, body: unknown): Promise<T> {
    const r = await fetch(this.baseUrl + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return (await r.json()) as T;
  }
}
