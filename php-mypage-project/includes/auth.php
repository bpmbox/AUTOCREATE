<?php
/**
 * ユーザー認証機能
 */

require_once 'config/database.php';
require_once 'config/session.php';
require_once 'includes/security.php';

class Auth {
    private $db;
    
    public function __construct() {
        $this->db = getDB();
    }
    
    /**
     * ユーザー登録
     */
    public function register($username, $email, $password, $full_name = '') {
        try {
            // 入力値チェック
            if (!$this->validateInput($username, $email, $password)) {
                return ['success' => false, 'message' => '入力値が不正です'];
            }
            
            // 重複チェック
            if ($this->userExists($username, $email)) {
                return ['success' => false, 'message' => 'ユーザー名またはメールアドレスが既に使用されています'];
            }
            
            // パスワードハッシュ化
            $password_hash = password_hash($password, PASSWORD_DEFAULT);
            
            // ユーザー作成
            $stmt = $this->db->prepare("
                INSERT INTO users (username, email, password_hash, full_name) 
                VALUES (?, ?, ?, ?)
            ");
            
            $stmt->execute([$username, $email, $password_hash, $full_name]);
            
            return ['success' => true, 'message' => 'ユーザー登録が完了しました'];
            
        } catch (Exception $e) {
            return ['success' => false, 'message' => 'エラーが発生しました: ' . $e->getMessage()];
        }
    }
    
    /**
     * ログイン
     */
    public function login($username, $password) {
        try {
            $stmt = $this->db->prepare("
                SELECT id, username, email, password_hash, full_name 
                FROM users 
                WHERE username = ? OR email = ?
            ");
            
            $stmt->execute([$username, $username]);
            $user = $stmt->fetch();
            
            if ($user && password_verify($password, $user['password_hash'])) {
                // セッション設定
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['username'] = $user['username'];
                $_SESSION['email'] = $user['email'];
                $_SESSION['full_name'] = $user['full_name'];
                
                // セッション再生成
                regenerateSession();
                
                return ['success' => true, 'message' => 'ログインしました'];
            } else {
                return ['success' => false, 'message' => 'ユーザー名またはパスワードが間違っています'];
            }
            
        } catch (Exception $e) {
            return ['success' => false, 'message' => 'エラーが発生しました: ' . $e->getMessage()];
        }
    }
    
    /**
     * ユーザー情報取得
     */
    public function getUserInfo($user_id) {
        try {
            $stmt = $this->db->prepare("
                SELECT id, username, email, full_name, bio, avatar_url, created_at 
                FROM users 
                WHERE id = ?
            ");
            
            $stmt->execute([$user_id]);
            return $stmt->fetch();
            
        } catch (Exception $e) {
            return false;
        }
    }
    
    /**
     * プロフィール更新
     */
    public function updateProfile($user_id, $full_name, $bio, $email) {
        try {
            $stmt = $this->db->prepare("
                UPDATE users 
                SET full_name = ?, bio = ?, email = ? 
                WHERE id = ?
            ");
            
            $stmt->execute([$full_name, $bio, $email, $user_id]);
            
            return ['success' => true, 'message' => 'プロフィールを更新しました'];
            
        } catch (Exception $e) {
            return ['success' => false, 'message' => 'エラーが発生しました: ' . $e->getMessage()];
        }
    }
    
    /**
     * パスワード変更
     */
    public function changePassword($user_id, $current_password, $new_password) {
        try {
            // 現在のパスワード確認
            $stmt = $this->db->prepare("SELECT password_hash FROM users WHERE id = ?");
            $stmt->execute([$user_id]);
            $user = $stmt->fetch();
            
            if (!password_verify($current_password, $user['password_hash'])) {
                return ['success' => false, 'message' => '現在のパスワードが間違っています'];
            }
            
            // 新しいパスワードをハッシュ化
            $new_password_hash = password_hash($new_password, PASSWORD_DEFAULT);
            
            // パスワード更新
            $stmt = $this->db->prepare("UPDATE users SET password_hash = ? WHERE id = ?");
            $stmt->execute([$new_password_hash, $user_id]);
            
            return ['success' => true, 'message' => 'パスワードを変更しました'];
            
        } catch (Exception $e) {
            return ['success' => false, 'message' => 'エラーが発生しました: ' . $e->getMessage()];
        }
    }
    
    /**
     * 入力値検証
     */
    private function validateInput($username, $email, $password) {
        return !empty($username) && 
               !empty($email) && 
               !empty($password) && 
               filter_var($email, FILTER_VALIDATE_EMAIL) &&
               strlen($password) >= 8;
    }
    
    /**
     * ユーザー存在チェック
     */
    private function userExists($username, $email) {
        $stmt = $this->db->prepare("
            SELECT COUNT(*) 
            FROM users 
            WHERE username = ? OR email = ?
        ");
        
        $stmt->execute([$username, $email]);
        return $stmt->fetchColumn() > 0;
    }
}
?>
